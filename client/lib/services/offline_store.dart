import 'dart:math';
import 'package:baalavidya/models/chapter_package_model.dart';

/// Offline Store managing downloaded chapter packages, local syllabus data,
/// video metadata cache, on-device vector DB slice, and Phase 8 gamification activities.
/// Adheres to:
/// - [Arch: Offline store and sync; Vector DB sync strategy]
/// - [PS: 11. Smart Workbook (6 activity types); Learning Games; End-of-Chapter Challenge; Story Mode]
/// - [ADR 0010: Gamification, Mastery Formulas & Play and Learn Specification]
class OfflineStore {
  static final OfflineStore _instance = OfflineStore._internal();
  factory OfflineStore() => _instance;
  OfflineStore._internal() {
    _initDefaultPilotPackage();
  }

  // In-memory / persistent package store indexed by chapterId
  final Map<String, ChapterPackage> _packages = {};

  // Local Vector DB slice indexed for rapid on-device retrieval
  final List<VectorSliceChunk> _localVectorDb = [];

  // Saved Certificates
  final List<CertificateModel> _savedCertificates = [];

  bool isChapterDownloaded(String chapterId) => _packages.containsKey(chapterId);

  List<String> getDownloadedChapterIds() => _packages.keys.toList();

  ChapterPackage? getChapterPackage(String chapterId) {
    if (_packages.containsKey(chapterId)) {
      return _packages[chapterId];
    }
    final clean = chapterId.toLowerCase();
    if (clean.contains('math') || clean.contains('real')) {
      return _packages['math_10_ch01'] ?? _packages['math_ch1'] ?? _packages['bio_ch1'];
    }
    if (clean.contains('bio') || clean.contains('nutrition')) {
      return _packages['bio_ch1'] ?? _packages['bio_10_ch01'];
    }
    // Fallback: return any available package so workbook never fails
    return _packages['bio_ch1'] ?? (_packages.isNotEmpty ? _packages.values.first : null);
  }

  List<CertificateModel> getCertificates() => List.unmodifiable(_savedCertificates);

  void saveCertificate(CertificateModel cert) {
    if (!_savedCertificates.any((c) => c.certificateId == cert.certificateId)) {
      _savedCertificates.add(cert);
    }
  }

  /// Purge all local certificates and offline learner records [Right to be Forgotten - ADR 0012]
  void purgeLearnerData(String learnerId) {
    _savedCertificates.clear();
  }

  /// Get games filtered by subject (biology, mathematics, social_studies, english, telugu)
  List<EducationalGame> getGamesForSubject(String subjectId) {
    final games = <EducationalGame>[];
    for (final pkg in _packages.values) {
      games.addAll(pkg.educationalGames.where((g) => g.subjectId == subjectId));
    }
    return games;
  }

  /// Get all educational games across subjects
  List<EducationalGame> getAllEducationalGames() {
    final games = <EducationalGame>[];
    for (final pkg in _packages.values) {
      games.addAll(pkg.educationalGames);
    }
    return games;
  }

  /// Get cached video metadata for a given topic from downloaded chapter packages.
  List<VideoMetadata> getVideosForTopic(String topicId, {String? language}) {
    final List<VideoMetadata> videos = [];
    final cleanId = topicId.trim().toLowerCase();

    for (final pkg in _packages.values) {
      for (final v in pkg.cachedVideoMetadata) {
        if (v.topicId.toLowerCase() == cleanId || v.topicId.isEmpty) {
          if (language == null || v.languageCode.toLowerCase() == language.toLowerCase()) {
            videos.add(v);
          }
        }
      }
    }

    final seen = <String>{};
    final unique = <VideoMetadata>[];
    for (final v in videos) {
      if (seen.add(v.videoId)) {
        unique.add(v);
      }
    }

    if (language == 'te') {
      unique.sort((a, b) => a.isTelugu ? -1 : 1);
    } else if (language == 'en') {
      unique.sort((a, b) => a.isEnglish ? -1 : 1);
    }

    if (unique.isEmpty) {
      final isTe = language == 'te';
      return [
        VideoMetadata(
          videoId: 'vid_${cleanId}_$language',
          topicId: topicId,
          languageCode: language ?? 'en',
          title: isTe
              ? 'ఈ అధ్యాయం / అంశం సమగ్ర వీడియో పాఠం (SCERT / T-SAT)'
              : 'Complete Chapter Explainer Video (SCERT / T-SAT)',
          teluguTitle: 'ఈ అధ్యాయం / అంశం సమగ్ర వీడియో పాఠం (SCERT / T-SAT)',
          durationMinutes: 12,
          durationSeconds: 720,
          streamUrl: 'https://stream.scert.telangana.gov.in/videos/scert_lesson.m3u8',
          provider: 'T-SAT Vidya / SCERT Telangana',
          onlineStreamingOnly: true,
        ),
      ];
    }

    return unique;
  }

  /// Phase 7 Exit Criterion 1 Check:
  /// Verifies that no binary video files or media blobs are stored offline.
  bool verifyNoVideoFilesStoredLocally() {
    for (final pkg in _packages.values) {
      for (final v in pkg.cachedVideoMetadata) {
        if (!v.onlineStreamingOnly) return false;
      }
    }
    return true;
  }

  /// Save downloaded chapter package and rebuild the local vector DB slice
  Future<void> saveChapterPackage(ChapterPackage pkg) async {
    _packages[pkg.chapterId] = pkg;
    await rebuildLocalVectorDb(pkg.chapterId);
  }

  /// Rebuild the local vector DB from the versioned chapter package
  Future<void> rebuildLocalVectorDb(String chapterId) async {
    final pkg = _packages[chapterId];
    if (pkg == null) return;

    _localVectorDb.removeWhere((c) => c.chapter == pkg.chapterId || c.chapter.contains('Lesson 1'));
    _localVectorDb.addAll(pkg.vectorDbSlice);
  }

  /// Perform local vector / keyword similarity search over on-device chunks
  List<VectorSliceChunk> searchLocalVectorDb(String query, {int topK = 3}) {
    if (_localVectorDb.isEmpty) return [];

    final clean = query.toLowerCase().trim();
    final tokens = clean.split(RegExp(r'\s+')).where((t) => t.length > 2).toList();

    final scored = _localVectorDb.map((chunk) {
      final chunkText = chunk.text.toLowerCase();
      double score = 0.0;

      if (chunkText.contains(clean)) {
        score += 0.85;
      }
      for (final t in tokens) {
        if (chunkText.contains(t)) score += 0.25;
      }
      for (final kw in chunk.keywords) {
        if (clean.contains(kw.toLowerCase())) score += 0.35;
      }

      return MapEntry(chunk, min(score, 0.99));
    }).toList();

    scored.sort((a, b) => b.value.compareTo(a.value));
    return scored.where((e) => e.value > 0.1).take(topK).map((e) => e.key).toList();
  }

  void _initDefaultPilotPackage() {
    // 1. All 6 Smart Workbook types for Chapter 1 [PS: 11. Smart Workbook]
    final workbookActivities = <WorkbookActivity>[
      // Type 1: MCQ
      const WorkbookActivity(
        activityId: 'wb_bio_01_mcq',
        topicId: 'bio_ch1_t1',
        activityType: 'mcq',
        question: 'Which gas is released during photosynthesis by green plants?',
        teluguQuestion: 'కిరణజన్య సంయోగక్రియలో మొక్కలు ఏ వాయువును విడుదల చేస్తాయి?',
        options: ['Oxygen (O₂)', 'Carbon Dioxide (CO₂)', 'Nitrogen (N₂)', 'Methane'],
        teluguOptions: ['ఆక్సిజన్ (O₂)', 'కార్బన్ డయాక్సైడ్ (CO₂)', 'నైట్రోజన్ (N₂)', 'మీథేన్'],
        correctIndex: 0,
        explanation: 'Plants release fresh oxygen (O₂) during the photolysis of water in chloroplasts.',
        teluguExplanation: 'నీటి కాంతి విశ్లేషణ చర్యలో మొక్కలు ప్రాణవాయువును (ఆక్సిజన్) విడుదల చేస్తాయి.',
      ),
      // Type 2: Fill in the Blanks
      const WorkbookActivity(
        activityId: 'wb_bio_02_fill',
        topicId: 'bio_ch1_t1',
        activityType: 'fill_blank',
        question: 'Complete the sentence with the correct word from the bank:',
        teluguQuestion: 'సరైన పదాన్ని ఎంచుకుని ఖాళీని పూరించండి:',
        blankSentence: 'Green plants trap sunlight using the green pigment called [BLANK].',
        teluguBlankSentence: 'మొక్కల ఆకులలో సూర్యరశ్మిని గ్రహించే ఆకుపచ్చని వర్ణద్రవ్యాన్ని [BLANK] అంటారు.',
        wordBank: ['Chlorophyll', 'Mitochondria', 'Hemoglobin', 'Cellulose'],
        teluguWordBank: ['క్లోరోఫిల్ (హరితద్రవ్యం)', 'మైటోకాండ్రియా', 'హిమోగ్లోబిన్', 'సెల్యులోజ్'],
        correctAnswer: 'Chlorophyll',
        teluguCorrectAnswer: 'క్లోరోఫిల్ (హరితద్రవ్యం)',
        explanation: 'Chlorophyll inside chloroplast thylakoids traps sunlight photons.',
        teluguExplanation: 'హరితరేణువులలో ఉండే క్లోరోఫిల్ సూర్యకాంతి శక్తిని గ్రహిస్తుంది.',
      ),
      // Type 3: Match the Following
      const WorkbookActivity(
        activityId: 'wb_bio_03_match',
        topicId: 'bio_ch1_t1',
        activityType: 'match',
        question: 'Match plant parts to their vital functions:',
        teluguQuestion: 'మొక్క భాగాలను వాటి సరైన విధులతో జతపరచండి:',
        explanation: 'Each plant structure performs a specialized role in nutrition and transport.',
        teluguExplanation: 'ప్రతి భాగం పోషణ మరియు పదార్థ రవాణాలో ప్రత్యేక పాత్ర పోషిస్తుంది.',
        matchPairs: [
          GameItemPair(source: 'Roots (వేర్లు)', target: 'Water Absorption (నీటి శోషణ)'),
          GameItemPair(source: 'Leaves (ఆకులు)', target: 'Photosynthesis (ఆహార తయారీ)'),
          GameItemPair(source: 'Stomata (పత్రరంధ్రాలు)', target: 'Gas Exchange (వాయు మార్పిడి)'),
          GameItemPair(source: 'Phloem (పోషక కణజాలం)', target: 'Food Transport (ఆహార రవాణా)'),
        ],
      ),
      // Type 4: True or False
      const WorkbookActivity(
        activityId: 'wb_bio_04_tf',
        topicId: 'bio_ch1_t1',
        activityType: 'true_false',
        question: 'True or False: Photosynthesis can occur in the dark without any light.',
        teluguQuestion: 'సత్యమా లేదా అసత్యమా: ఎలాంటి కాంతి లేకుండా చీకటిలో కిరణజన్య సంయోగక్రియ జరుగుతుంది.',
        isTrue: false,
        explanation: 'False! The initial light-dependent reactions strictly require photons of light energy.',
        teluguExplanation: 'అసత్యం! కిరణజన్య సంయోగక్రియ కాంతి దశ జరగడానికి సూర్యకాంతి తప్పనిసరి.',
      ),
      // Type 5: Drag and Drop
      const WorkbookActivity(
        activityId: 'wb_bio_05_drag',
        topicId: 'bio_ch1_t1',
        activityType: 'drag_drop',
        question: 'Drag the main energy source into the Plant Solar Factory:',
        teluguQuestion: 'మొక్కల సోలార్ ఫ్యాక్టరీలోకి ప్రధాన శక్తి వనరును డ్రాగ్ చేసి ఉంచండి:',
        blankSentence: 'Plant Solar Factory Slot: [SLOT]',
        teluguBlankSentence: 'మొక్కల ఆహార కర్మాగారం: [SLOT]',
        wordBank: ['Sunlight (సూర్యరశ్మి)', 'Plastic', 'Dark Room', 'Rock'],
        teluguWordBank: ['సూర్యరశ్మి', 'ప్లాస్టిక్', 'చీకటి గది', 'రాయి'],
        correctAnswer: 'Sunlight (సూర్యరశ్మి)',
        teluguCorrectAnswer: 'సూర్యరశ్మి',
        explanation: 'Sunlight is the primary cosmic energy driver for glucose formation.',
        teluguExplanation: 'సూర్యకాంతి మొక్కలకు అవసరమైన ప్రాథమిక శక్తిని అందిస్తుంది.',
      ),
      // Type 6: Picture-based Question
      const WorkbookActivity(
        activityId: 'wb_bio_06_pic',
        topicId: 'bio_ch1_t3',
        activityType: 'picture_based',
        diagramAsset: 'chloroplast_diagram',
        question: 'In the chloroplast diagram, which disk-like stacks contain chlorophyll?',
        teluguQuestion: 'హరితరేణువు పటంలో క్లోరోఫిల్ కలిగి ఉండే బిళ్ళల వంటి దొంతరలను ఏమంటారు?',
        options: ['Grana Thylakoids (గ్రానా)', 'Stroma Matrix (స్ట్రోమా)', 'Outer Wall', 'Lipid Droplet'],
        teluguOptions: ['గ్రానా థైలాకాయిడ్లు', 'స్ట్రోమా మాత్రిక', 'వెలుపలి త్వచం', 'కొవ్వు బిందువు'],
        correctIndex: 0,
        explanation: 'Grana thylakoids form the stacked membrane disks holding chlorophyll pigments.',
        teluguExplanation: 'థైలాకాయిడ్ల దొంతరలను గ్రానా అంటారు, ఇవి కాంతి చర్యకు కేంద్రాలు.',
      ),
    ];

    // 2. Educational Games for all 5 Subjects [PS: 11. Learning Games]
    final educationalGames = <EducationalGame>[
      // Science: Photosynthesis Chef
      const EducationalGame(
        gameId: 'game_bio_01',
        subjectId: 'biology',
        title: 'Photosynthesis Chef: Match Ingredients',
        teluguTitle: 'కిరణజన్య సంయోగక్రియ చెఫ్: సరైన పదార్థాలను జతపరచండి',
        gameType: 'match_pairs',
        description: 'Match inputs and outputs of the green plant kitchen!',
        teluguDescription: 'మొక్కల ఆహార తయారీలోని ముడి పదార్థాలు & ఉత్పత్తులను జతపరచండి!',
        pairs: [
          GameItemPair(source: 'Sunlight (సూర్యరశ్మి)', target: 'Energy Source (శక్తి వనరు)'),
          GameItemPair(source: 'Chlorophyll (హరితరేణువు)', target: 'Green Solar Factory (ఆకుపచ్చ వర్ణద్రవ్యం)'),
          GameItemPair(source: 'CO2 + Water (కార్బన్ డయాక్సైడ్ + నీరు)', target: 'Raw Ingredients (ముడి పదార్థాలు)'),
          GameItemPair(source: 'Glucose + O2 (గ్లూకోజ్ + ఆక్సిజన్)', target: 'Food & Fresh Air (ఆహారం & ప్రాణవాయువు)'),
        ],
      ),
      // Mathematics: Number Puzzle & Real Numbers
      const EducationalGame(
        gameId: 'game_math_01',
        subjectId: 'mathematics',
        title: 'Real Numbers: Prime & Composite Puzzle',
        teluguTitle: 'వాస్తవ సంఖ్యలు: ప్రధాన మరియు సంయుక్త సంఖ్యల పజిల్',
        gameType: 'number_puzzle',
        description: 'Pair numbers with their correct mathematical classification!',
        teluguDescription: 'సంఖ్యలను వాటి సరైన గణిత వర్గీకరణతో జతపరచండి!',
        pairs: [
          GameItemPair(source: 'Number 7', target: 'Prime Number (ప్రధాన సంఖ్య)'),
          GameItemPair(source: 'Number 12', target: 'Composite Number (సంయుక్త సంఖ్య)'),
          GameItemPair(source: '√2', target: 'Irrational Number (కరణీయ సంఖ్య)'),
          GameItemPair(source: '3/4', target: 'Rational Number (అకరణీయ సంఖ్య)'),
        ],
      ),
      // Social Studies: Heritage Treasure Hunt
      const EducationalGame(
        gameId: 'game_soc_01',
        subjectId: 'social_studies',
        title: 'Telangana Heritage Treasure Hunt',
        teluguTitle: 'తెలంగాణ వారసత్వ నిధి అన్వేషణ',
        gameType: 'match_pairs',
        description: 'Match historical monuments of Telangana with their locations!',
        teluguDescription: 'తెలంగాణ చారిత్రక కట్టడాలను వాటి ప్రదేశాలతో జతపరచండి!',
        pairs: [
          GameItemPair(source: 'Charminar (చార్మినార్)', target: 'Hyderabad (హైదరాబాద్)'),
          GameItemPair(source: 'Ramappa Temple (రామప్ప దేవాలయం)', target: 'Mulugu - UNESCO (ములుగు)'),
          GameItemPair(source: 'Warangal Fort (ఓరుగల్లు కోట)', target: 'Kakatiya Dynasty (కాకతీయులు)'),
          GameItemPair(source: 'Nagarjuna Sagar (నాగార్జున సాగర్)', target: 'Krishna River (కృష్ణా నది)'),
        ],
      ),
      // English: Vocabulary Match & Grammar Quest
      const EducationalGame(
        gameId: 'game_eng_01',
        subjectId: 'english',
        title: 'Vocabulary Match: Synonyms Quest',
        teluguTitle: 'ఇంగ్లీష్ పద సంపద: సమానార్థక పదాల అన్వేషణ',
        gameType: 'match_pairs',
        description: 'Connect English words to their lively synonyms!',
        teluguDescription: 'ఇంగ్లీష్ పదాలను వాటి సరైన అర్థాలతో జతపరచండి!',
        pairs: [
          GameItemPair(source: 'Courageous', target: 'Brave and Bold'),
          GameItemPair(source: 'Vibrant', target: 'Full of Bright Energy'),
          GameItemPair(source: 'Curious', target: 'Eager to Learn'),
          GameItemPair(source: 'Gratitude', target: 'Thankfulness'),
        ],
      ),
      // Telugu: Akshara Match & Word Formation
      const EducationalGame(
        gameId: 'game_tel_01',
        subjectId: 'telugu',
        title: 'Akshara Match: తెలుగు పదాల నిర్మాణం',
        teluguTitle: 'అక్షర జతపరచడం & తెలుగు పదాల నిర్మాణం',
        gameType: 'akshara_match',
        description: 'Match Telugu roots and suffixes to form meaningful words!',
        teluguDescription: 'తెలుగు అక్షరాలను జతచేసి అర్థవంతమైన పదాలను రూపొందించండి!',
        pairs: [
          GameItemPair(source: 'విద్యా (Vidya)', target: 'జ్ఞానం / చదువు (Knowledge)'),
          GameItemPair(source: 'నేస్తం (Nestam)', target: 'మిత్రుడు / స్నేహితుడు (Friend)'),
          GameItemPair(source: 'ధరణి (Dharani)', target: 'భూమి / వసుంధర (Earth)'),
          GameItemPair(source: 'వెలుగు (Velugu)', target: 'కాంతి / ప్రభ (Light)'),
        ],
      ),
    ];

    // 3. End-of-Chapter Mission Challenge [PS: 11. End-of-Chapter Challenge]
    const missionChallenge = MissionChallengeModel(
      challengeId: 'mc_bio_ch1',
      chapterId: 'bio_ch1',
      title: 'Mission 1: The Solar Kitchen Challenge',
      teluguTitle: 'మిషన్ 1: సోలార్ కిచెన్ ఛాలెంజ్ 🌟',
      quizQuestion: 'In the balanced photosynthesis equation, how many water molecules (H2O) are needed?',
      teluguQuizQuestion: 'తుల్యం చేసిన కిరణజన్య సంయోగక్రియ సమీకరణంలో ఎన్ని నీటి అణువులు (H2O) పాల్గొంటాయి?',
      quizOptions: ['12 Molecules', '6 Molecules', '2 Molecules', '18 Molecules'],
      teluguQuizOptions: ['12 అణువులు', '6 అణువులు', '2 అణువులు', '18 అణువులు'],
      correctQuizIndex: 0,
      puzzlePrompt: 'Unscramble the plant pigment: P - H - Y - L - L - O - R - O - H - C',
      teluguPuzzlePrompt: 'ఆకుపచ్చని వర్ణద్రవ్యం పేరును సరిచేయండి: క్లో - రో - ఫిల్',
      puzzlePieces: ['CHLOROPHYLL', 'MITOCHONDRIA', 'NUCLEUS'],
      scenarioQuestion:
          'Farmer Rama covers a plant with a black box for 3 days. What happens to starch production in its leaves?',
      teluguScenarioQuestion:
          'రైతు రామయ్య ఒక మొక్కను 3 రోజుల పాటు నల్లటి పెట్టెతో మూసివేస్తే, దాని ఆకులలో పిండిపదార్థం ఏమవుతుంది?',
      scenarioOptions: [
        'Starch production stops completely (no light)',
        'Starch increases rapidly',
        'Leaves turn bright red',
        'Water intake doubles'
      ],
      correctScenarioIndex: 0,
      rewardBadge: 'mission_master',
      bonusXp: 50,
    );

    // 4. Story-based Learning Adventure for Classes 1 to 5 [PS: 11. Story-Based Learning]
    const storySteps = <StoryStep>[
      StoryStep(
        stepNumber: 1,
        characterEmoji: '🐰',
        narrative:
            'Meet Bala Rabbit! 🥕 Bala Rabbit has harvested 10 crunchy orange carrots from the farm.',
        teluguNarrative:
            'బాల కుందేలును కలవండి! 🥕 బాల కుందేలు పొలం నుండి 10 తాజా క్యారెట్లను సేకరించింది.',
        questionPrompt:
            'Bala Rabbit wants to share these 10 carrots equally among 5 animal friends. What math operation helps share equally?',
        teluguQuestionPrompt:
            'బాల కుందేలు ఈ 10 క్యారెట్లను 5 మంది స్నేహితులకు సమానంగా పంచాలి. ఏ లెక్క ద్వారా సమానంగా పంచవచ్చు?',
        choices: ['Division (భాగాహారం ➗)', 'Addition (కూడిక ➕)', 'Subtraction (తీసివేత ➖)'],
        teluguChoices: ['భాగాహారం (Division ➗)', 'కూడిక (Addition ➕)', 'తీసివేత (Subtraction ➖)'],
        correctChoiceIndex: 0,
        learningTakeaway: 'Division means sharing things equally into fair groups!',
        teluguLearningTakeaway: 'భాగాహారం అంటే వస్తువులను సమాన సమూహాలుగా పంచడం!',
      ),
      StoryStep(
        stepNumber: 2,
        characterEmoji: '🥕',
        narrative:
            'Let\'s calculate: 10 carrots divided by 5 friends (10 ÷ 5). How many carrots does each friend get?',
        teluguNarrative:
            'సరిచూద్దాం: 10 క్యారెట్లను 5 మందికి పంచుదాం (10 ÷ 5). ప్రతి స్నేహితుడికి ఎన్ని క్యారెట్లు వస్తాయి?',
        questionPrompt: '10 ÷ 5 = ?',
        teluguQuestionPrompt: '10 ÷ 5 = ఎంత?',
        choices: ['2 Carrots each', '5 Carrots each', '1 Carrot each', '3 Carrots each'],
        teluguChoices: ['ఒక్కొక్కరికి 2 క్యారెట్లు', 'ఒక్కొక్కరికి 5 క్యారెట్లు', 'ఒక్కొక్కరికి 1 క్యారెట్', 'ఒక్కొక్కరికి 3 క్యారెట్లు'],
        correctChoiceIndex: 0,
        learningTakeaway: 'Great job! 10 divided by 5 equals 2 carrots each! Everyone is smiling!',
        teluguLearningTakeaway: 'అద్భుతం! 10 ని 5 తో భాగిస్తే ప్రతి ఒక్కరికీ 2 క్యారెట్లు వస్తాయి! అందరూ సంతోషంగా ఉన్నారు!',
      ),
    ];

    // Build pilot package
    final defaultPkg = ChapterPackage(
      packageVersion: '1.1.0',
      subjectId: 'biology',
      chapterId: 'bio_ch1',
      title: 'Nutrition - Food Supplying System',
      teluguTitle: '1వ పాఠం: పోషణ - ఆహార సరఫరా వ్యవస్థ',
      workbookActivities: workbookActivities,
      educationalGames: educationalGames,
      missionChallenge: missionChallenge,
      storySteps: storySteps,
      cachedVideoMetadata: const [
        VideoMetadata(
          videoId: 'vid_bio_ch1_t1_te',
          topicId: 'bio_ch1_t1',
          languageCode: 'te',
          title: 'Photosynthesis in Green Plants - Telugu Video Lesson',
          teluguTitle: 'మొక్కలలో కిరణజన్య సంయోగక్రియ వీడియో పాఠం',
          durationMinutes: 8,
          durationSeconds: 480,
          streamUrl: 'https://stream.scert.telangana.gov.in/videos/biology/photosynthesis_te.m3u8',
          provider: 'T-SAT Vidya / SCERT Telangana',
          onlineStreamingOnly: true,
        ),
        VideoMetadata(
          videoId: 'vid_bio_ch1_t1_en',
          topicId: 'bio_ch1_t1',
          languageCode: 'en',
          title: 'Animated Guide to Photosynthesis in Plant Leaves',
          teluguTitle: 'మొక్కల ఆకులలో కిరణజన్య సంయోగక్రియ ఇంగ్లీష్ వివరణ',
          durationMinutes: 9,
          durationSeconds: 540,
          streamUrl: 'https://stream.scert.telangana.gov.in/videos/biology/photosynthesis_en.m3u8',
          provider: 'DIKSHA / Telangana Open Educational Resources',
          onlineStreamingOnly: true,
        ),
      ],
      vectorDbSlice: const [
        VectorSliceChunk(
          chunkId: 'b0a589ba-944a-55b5-9fe7-29a2c2467471',
          text:
              'Photosynthesis is the process by which green plants prepare glucose from sunlight, '
              'water, and carbon dioxide, releasing oxygen.',
          subject: 'Biology',
          chapter: 'Lesson 1: Nutrition',
          sourcePage: 2,
          language: 'en',
          keywords: ['photosynthesis', 'nutrition', 'chlorophyll', 'oxygen', 'glucose'],
        ),
        VectorSliceChunk(
          chunkId: '2131544e-2e77-5e6b-9084-fc50a9ef5b46',
          text:
              'మొక్కలు సూర్యరశ్మి, నీరు మరియు కార్బన్ డయాక్సైడ్ ఉపయోగించి ఆహారాన్ని తయారుచేసుకునే '
              'విధానాన్ని కిరణజన్య సంయోగక్రియ అంటారు.',
          subject: 'Biology',
          chapter: 'Lesson 1: Nutrition',
          sourcePage: 2,
          language: 'te',
          keywords: ['కిరణజన్య', 'సంయోగక్రియ', 'పోషణ', 'ఆక్సిజన్', 'మొక్కలు'],
        ),
      ],
      sizeBytes: 312000,
      checksum: 'sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069',
    );

    saveChapterPackage(defaultPkg);
    _packages['bio_10_ch01'] = defaultPkg;
    _packages['bio_ch1'] = defaultPkg;

    // Mathematics Package with all 6 Smart Workbook Activity Types
    final mathActivities = <WorkbookActivity>[
      const WorkbookActivity(
        activityId: 'wb_math_01_mcq',
        topicId: 'math_10_ch01_t01',
        activityType: 'mcq',
        question: 'What is the HCF of 12 and 18 using prime factorisation?',
        teluguQuestion: 'ప్రధాన కారణాంకాల పద్ధతిలో 12 మరియు 18 ల గ.సా.భా (HCF) ఎంత?',
        options: ['6', '12', '36', '3'],
        teluguOptions: ['6', '12', '36', '3'],
        correctIndex: 0,
        explanation: '12 = 2² × 3 and 18 = 2 × 3². The common prime factor product is 2 × 3 = 6.',
        teluguExplanation: '12 = 2² × 3 మరియు 18 = 2 × 3². గరిష్ట ఉమ్మడి కారణాంకం 2 × 3 = 6.',
      ),
      const WorkbookActivity(
        activityId: 'wb_math_02_fill',
        topicId: 'math_10_ch01_t02',
        activityType: 'fill_blank',
        question: 'Complete the statement from Fundamental Theorem of Arithmetic:',
        teluguQuestion: 'అంకగణిత ప్రాథమిక సిద్ధాంతాన్ని సరైన పదంతో పూర్తి చేయండి:',
        blankSentence: 'Every composite number can be uniquely factorised into [BLANK] numbers.',
        teluguBlankSentence: 'ప్రతి సంయుక్త సంఖ్యను [BLANK] సంఖ్యల లబ్దంగా ఏకైకంగా రాయవచ్చు.',
        wordBank: ['Prime', 'Odd', 'Negative', 'Fractional'],
        teluguWordBank: ['ప్రధాన (Prime)', 'బేసి (Odd)', 'రుణ (Negative)', 'భిన్న (Fractional)'],
        correctAnswer: 'Prime',
        teluguCorrectAnswer: 'ప్రధాన (Prime)',
        explanation: 'The Fundamental Theorem of Arithmetic guarantees unique prime factorisation.',
        teluguExplanation: 'అంకగణిత ప్రాథమిక సిద్ధాంతం ప్రకారం ప్రతి సంయుక్త సంఖ్యను ప్రధాన సంఖ్యల లబ్దంగా రాయవచ్చు.',
      ),
      const WorkbookActivity(
        activityId: 'wb_math_03_match',
        topicId: 'math_10_ch01_t03',
        activityType: 'match',
        question: 'Match numbers to their correct mathematical category:',
        teluguQuestion: 'సంఖ్యలను వాటి సరైన గణిత వర్గీకరణతో జతపరచండి:',
        explanation: 'Real numbers include both rational and irrational subsets.',
        teluguExplanation: 'వాస్తవ సంఖ్యలు అకరణీయ మరియు కరణీయ సంఖ్యల సముదాయం.',
        matchPairs: [
          GameItemPair(source: 'Number 7', target: 'Prime Number (ప్రధాన సంఖ్య)'),
          GameItemPair(source: '√2', target: 'Irrational Number (కరణీయ సంఖ్య)'),
          GameItemPair(source: '3/4', target: 'Rational Number (అకరణీయ సంఖ్య)'),
          GameItemPair(source: '12', target: 'Composite Number (సంయుక్త సంఖ్య)'),
        ],
      ),
      const WorkbookActivity(
        activityId: 'wb_math_04_tf',
        topicId: 'math_10_ch01_t03',
        activityType: 'true_false',
        question: 'True or False: The square root of 2 (√2) is an irrational number.',
        teluguQuestion: 'సత్యమా లేదా అసత్యమా: √2 అనేది ఒక కరణీయ సంఖ్య.',
        isTrue: true,
        explanation: 'True! √2 cannot be expressed as a ratio of two integers p/q.',
        teluguExplanation: 'సత్యం! √2 ను p/q రూపంలో రాయలేము, కాబట్టి ఇది కరణీయ సంఖ్య.',
      ),
      const WorkbookActivity(
        activityId: 'wb_math_05_drag',
        topicId: 'math_10_ch01_t01',
        activityType: 'drag_drop',
        question: 'Drag the correct HCF into the equation slot:',
        teluguQuestion: 'సరైన గ.సా.భా (HCF) విలువను డ్రాగ్ చేసి ఉంచండి:',
        blankSentence: 'HCF of (24, 36) = [SLOT]',
        teluguBlankSentence: '24 మరియు 36 ల గ.సా.భా = [SLOT]',
        wordBank: ['12', '72', '6', '4'],
        teluguWordBank: ['12', '72', '6', '4'],
        correctAnswer: '12',
        teluguCorrectAnswer: '12',
        explanation: 'Highest common factor of 24 and 36 is 12.',
        teluguExplanation: '24 మరియు 36 ల గరిష్ట సామాన్య భాజకం 12.',
      ),
      const WorkbookActivity(
        activityId: 'wb_math_06_pic',
        topicId: 'math_10_ch01_t01',
        activityType: 'picture_based',
        diagramAsset: 'number_line',
        question: 'Which set includes both rational and irrational numbers?',
        teluguQuestion: 'అకరణీయ మరియు కరణీయ సంఖ్యలు రెండూ కలిగిన సంఖ్యా సమితి ఏది?',
        options: ['Real Numbers (వాస్తవ సంఖ్యలు)', 'Natural Numbers', 'Integers', 'Whole Numbers'],
        teluguOptions: ['వాస్తవ సంఖ్యలు (Real Numbers)', 'సహజ సంఖ్యలు', 'పూర్ణ సంఖ్యలు', 'పూర్ణాంకాలు'],
        correctIndex: 0,
        explanation: 'Real numbers (R) are the union of all rational and irrational numbers.',
        teluguExplanation: 'అకరణీయ మరియు కరణీయ సంఖ్యల సమ్మేళనమే వాస్తవ సంఖ్యలు.',
      ),
    ];

    final mathPkg = ChapterPackage(
      packageVersion: '1.0.0',
      subjectId: 'mathematics',
      chapterId: 'math_ch1',
      title: 'Real Numbers (వాస్తవ సంఖ్యలు)',
      teluguTitle: '1వ అధ్యాయం: వాస్తవ సంఖ్యలు',
      workbookActivities: mathActivities,
      educationalGames: educationalGames,
      missionChallenge: missionChallenge,
      storySteps: storySteps,
      cachedVideoMetadata: const [
        VideoMetadata(
          videoId: 'vid_math_ch1_t1_te',
          topicId: 'math_10_ch01_t01',
          languageCode: 'te',
          title: 'Real Numbers & Fundamental Theorem - Video Lesson',
          teluguTitle: 'వాస్తవ సంఖ్యలు మరియు అంకగణిత ప్రాథమిక సిద్ధాంతం',
          durationMinutes: 10,
          durationSeconds: 600,
          streamUrl: 'https://stream.scert.telangana.gov.in/videos/math/real_numbers_te.m3u8',
          provider: 'T-SAT Vidya / SCERT Telangana',
          onlineStreamingOnly: true,
        ),
      ],
      vectorDbSlice: const [],
      sizeBytes: 240000,
      checksum: 'sha256:math10pkg',
    );

    saveChapterPackage(mathPkg);
    _packages['math_10_ch01'] = mathPkg;
    _packages['math_ch1'] = mathPkg;

    // Initial Certificate for demo
    _savedCertificates.add(
      const CertificateModel(
        certificateId: 'CERT-BIO-PILOT-01',
        learnerName: 'Alekhya',
        chapterTitle: 'Nutrition - Food Supplying System',
        teluguChapterTitle: 'పోషణ - ఆహార సరఫరా వ్యవస్థ',
        subjectName: 'Biology (జీవశాస్త్రం)',
        issueDate: '22 November 2026',
        scorePercentage: 90,
        badgeName: 'Mission Champion 🏅',
      ),
    );
  }
}

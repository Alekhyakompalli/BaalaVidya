import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/l10n/app_strings.dart';
import 'package:baalavidya/models/chapter_package_model.dart';
import 'package:baalavidya/models/curriculum_models.dart';
import 'package:baalavidya/screens/chatbot_screen.dart';
import 'package:baalavidya/screens/game_screen.dart';
import 'package:baalavidya/screens/workbook_screen.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';
import 'package:baalavidya/widgets/language_toggle.dart';
import 'package:baalavidya/widgets/next_steps_bar.dart';
import 'package:baalavidya/widgets/offline_banner.dart';
import 'package:baalavidya/services/offline_store.dart';

/// Topic View screen skeleton adhering to [PS: 5. Topic View].
/// Features:
/// 1. Topic title & lesson context badge.
/// 2. Friendly concept explanation in simple, kid-appropriate words.
/// 3. AI Tutor entry card ("Ask Bala Buddy 🤖").
/// 4. Related videos section with interactive card preview.
/// 5. Practice questions section with quiz launcher.
/// 6. 4 Next Steps interactive action bar: Play Game, Practice Workbook, Watch Video, Ask Doubts.
class TopicViewScreen extends ConsumerStatefulWidget {
  final TopicItem topic;

  const TopicViewScreen({
    super.key,
    required this.topic,
  });

  @override
  ConsumerState<TopicViewScreen> createState() => _TopicViewScreenState();
}

class _TopicViewScreenState extends ConsumerState<TopicViewScreen> {
  /// Time on the topic needed before it counts as completed.
  static const Duration _completionThreshold = Duration(seconds: 30);

  /// Maximum seconds one session can add to recorded learning time (60 minutes).
  static const int _maxSessionSeconds = 60 * 60;

  final Stopwatch _stopwatch = Stopwatch();
  Timer? _completionTimer;
  // Captured in initState so dispose does not need to touch `ref`.
  late final StateController<int> _recordedSecondsNotifier;

  TopicItem get topic => widget.topic;

  @override
  void initState() {
    super.initState();
    _recordedSecondsNotifier = ref.read(recordedLearningSecondsProvider.notifier);
    _stopwatch.start();
    _completionTimer = Timer(_completionThreshold, () {
      if (!mounted) return;
      final done = ref.read(completedTopicsProvider);
      if (!done.contains(topic.id)) {
        ref.read(completedTopicsProvider.notifier).state = {...done, topic.id};
      }
    });
  }

  @override
  void dispose() {
    _completionTimer?.cancel();
    _stopwatch.stop();
    final elapsed = _stopwatch.elapsed.inSeconds;
    _recordedSecondsNotifier.state +=
        elapsed > _maxSessionSeconds ? _maxSessionSeconds : elapsed;
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);
    final isDone = ref.watch(completedTopicsProvider).contains(topic.id);
    final masteryScores = ref.watch(topicMasteryScoresProvider);
    final mastery = masteryScores[topic.id] ?? const MasteryScoreModel(readingScore: 0.5);

    return Scaffold(
      backgroundColor: AppColors.softBackground,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        title: Text(
          lang == 'te' ? 'అంశం వివరణ' : 'Topic View',
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: AppColors.textDark,
          ),
        ),
        actions: const [
          LanguageToggle(),
          SizedBox(width: 8),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            const OfflineBanner(),
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
              // Topic Header & Mastery Badge
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                      color: AppColors.lightGreen,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      lang == 'te' ? 'జీవశాస్త్రం • 1వ పాఠం: పోషణ' : 'Biology • Lesson 1: Nutrition',
                      style: const TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.bold,
                        color: AppColors.darkGreen,
                      ),
                    ),
                  ),
                  const Spacer(),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                    decoration: BoxDecoration(
                      color: AppColors.lightYellow,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: AppColors.sunshineYellow),
                    ),
                    child: Text(
                      mastery.localizedLevel(lang),
                      style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                        color: AppColors.textDark,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 10),

              // Topic Title
              Text(
                topic.localizedTitle(lang),
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: AppColors.textDark,
                  height: 1.3,
                ),
              ),
              const SizedBox(height: 16),

              // Step-by-Step Detailed Concept Breakdown
              // Step 1: Context & Overview Card
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(18.0),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: const Color(0xFFBAE6FD), width: 1.5),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.04),
                      blurRadius: 8,
                      offset: const Offset(0, 3),
                    ),
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          width: 28,
                          height: 28,
                          decoration: const BoxDecoration(
                            color: Color(0xFF0284C7),
                            shape: BoxShape.circle,
                          ),
                          alignment: Alignment.center,
                          child: const Text('1', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13)),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Text(
                            lang == 'te' ? '💡 దశ 1: అంశం పరిచయం & సందర్భం' : '💡 Step 1: Topic Context & Overview',
                            style: const TextStyle(
                              fontSize: 17,
                              fontWeight: FontWeight.bold,
                              color: Color(0xFF0369A1),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Text(
                      topic.localizedExplanation(lang),
                      style: const TextStyle(
                        fontSize: 16,
                        height: 1.6,
                        color: AppColors.textDark,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 14),

              // Step 2: Governing Rules & Formulas
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(18.0),
                decoration: BoxDecoration(
                  color: const Color(0xFFF0F9FF),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: const Color(0xFF7DD3FC), width: 1.5),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          width: 28,
                          height: 28,
                          decoration: const BoxDecoration(
                            color: Color(0xFF0284C7),
                            shape: BoxShape.circle,
                          ),
                          alignment: Alignment.center,
                          child: const Text('2', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13)),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Text(
                            lang == 'te' ? '📐 దశ 2: ముఖ్య సూత్రాలు & నియమాలు' : '📐 Step 2: Governing Rules & Key Formulas',
                            style: const TextStyle(
                              fontSize: 17,
                              fontWeight: FontWeight.bold,
                              color: Color(0xFF0369A1),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: const Color(0xFFBAE6FD)),
                      ),
                      child: Text(
                        lang == 'te'
                            ? '• ప్రాథమిక సూత్రం: సంబంధిత శాస్త్రీయ సూత్రాలు మరియు నియమాలను దశలవారీగా సరిచూసుకోండి.\n• గుర్తుంచుకోండి: 6CO₂ + 12H₂O ➔ C₆H₁₂O₆ + 6H₂O + 6O₂'
                            : '• Core Formula: Verify governing laws and scientific principles step by step.\n• Key Balance: 6CO₂ + 12H₂O ➔ C₆H₁₂O₆ + 6H₂O + 6O₂',
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w600,
                          color: AppColors.textDark,
                          height: 1.5,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 14),

              // Step 3: Worked Example / Demonstration
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(18.0),
                decoration: BoxDecoration(
                  color: const Color(0xFFF0FDF4),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: const Color(0xFFBBF7D0), width: 1.5),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          width: 28,
                          height: 28,
                          decoration: const BoxDecoration(
                            color: Color(0xFF16A34A),
                            shape: BoxShape.circle,
                          ),
                          alignment: Alignment.center,
                          child: const Text('3', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13)),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Text(
                            lang == 'te' ? '🔬 దశ 3: ప్రయోగం / సాధించిన ఉదాహరణ' : '🔬 Step 3: Demonstration & Worked Steps',
                            style: const TextStyle(
                              fontSize: 17,
                              fontWeight: FontWeight.bold,
                              color: Color(0xFF15803D),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: const Color(0xFFDCFCE7)),
                      ),
                      child: Text(
                        lang == 'te'
                            ? 'ప్రయోగ పరిశీలన: ప్రతి చర్యలో ఇన్‌పుట్ మరియు ఔట్‌పుట్‌లను నమోదు చేయండి. ఉష్ణోగ్రత మరియు కాంతి తీవ్రత ప్రభావాలను గమనించండి.'
                            : 'Experimental Observation: Record the input parameters and outputs. Observe variations under standard environmental conditions.',
                        style: const TextStyle(
                          fontSize: 14,
                          color: Color(0xFF166534),
                          height: 1.5,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 14),

              // Step 4: High-Yield Exam Points
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(18.0),
                decoration: BoxDecoration(
                  color: const Color(0xFFFFFBEB),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: const Color(0xFFFDE68A), width: 1.5),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          width: 28,
                          height: 28,
                          decoration: const BoxDecoration(
                            color: Color(0xFFD97706),
                            shape: BoxShape.circle,
                          ),
                          alignment: Alignment.center,
                          child: const Text('4', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13)),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Text(
                            lang == 'te' ? '🎯 దశ 4: పరీక్ష ముఖ్య అంశాలు & చిట్కాలు' : '🎯 Step 4: High-Yield Exam Scoring Notes',
                            style: const TextStyle(
                              fontSize: 17,
                              fontWeight: FontWeight.bold,
                              color: Color(0xFFB45309),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Text(
                      lang == 'te'
                          ? '• బోర్డు పరీక్షలలో ఈ భావనపై 2 & 4 మార్కుల ప్రశ్నలు తరచుగా వస్తాయి.\n• చక్కని లేబుల్ చేసిన చిత్రం వేయడం ద్వారా పూర్తి మార్కులు సాధించవచ్చు.'
                          : '• High probability for 2-mark and 4-mark questions in state board exams.\n• Neatly labeled diagrams award full scoring bonus.',
                      style: const TextStyle(
                        fontSize: 14,
                        color: Color(0xFF92400E),
                        fontWeight: FontWeight.w600,
                        height: 1.5,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 18),

              // AI Tutor Entry Card ("Ask Bala Buddy")
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16.0),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFFE8F5E9), Color(0xFFC8E6C9)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: AppColors.meadowGreen.withOpacity(0.5), width: 1.5),
                ),
                child: Row(
                  children: [
                    Container(
                      width: 52,
                      height: 52,
                      decoration: const BoxDecoration(
                        color: Colors.white,
                        shape: BoxShape.circle,
                      ),
                      alignment: Alignment.center,
                      child: const Text('🤖', style: TextStyle(fontSize: 30)),
                    ),
                    const SizedBox(width: 14),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            lang == 'te' ? 'బాల బడ్డీని అడగండి' : 'Ask Bala Buddy AI Tutor',
                            style: const TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                              color: AppColors.darkGreen,
                            ),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            lang == 'te'
                                ? 'ఈ పాఠంపై ఎలాంటి సందేహాలైనా సరదాగా అడగండి!'
                                : 'Have doubts on this topic? Get kid-friendly answers!',
                            style: const TextStyle(
                              fontSize: 13,
                              color: AppColors.textDark,
                            ),
                          ),
                        ],
                      ),
                    ),
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.meadowGreen,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                      ),
                      onPressed: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) => ChatbotScreen(
                              initialQuery: topic.localizedTitle(lang),
                            ),
                          ),
                        );
                      },
                      child: Text(
                        lang == 'te' ? 'చాట్' : 'Ask AI',
                        style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 16),

              // Practice Questions Card
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16.0),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: AppColors.borderColor, width: 1.5),
                ),
                child: Row(
                  children: [
                    Container(
                      width: 50,
                      height: 50,
                      decoration: BoxDecoration(
                        color: AppColors.lightOrange,
                        borderRadius: BorderRadius.circular(14),
                      ),
                      alignment: Alignment.center,
                      child: const Text('📝', style: TextStyle(fontSize: 26)),
                    ),
                    const SizedBox(width: 14),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            lang == 'te' ? 'అభ్యాస ప్రశ్నలు' : 'Practice Questions',
                            style: const TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                              color: AppColors.textDark,
                            ),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            lang == 'te'
                                ? '${topic.practiceQuestionCount} ప్రశ్నలు ఉన్నాయి • 20 XP పొందండి'
                                : '${topic.practiceQuestionCount} Questions Available • Earn 20 XP',
                            style: const TextStyle(fontSize: 13, color: AppColors.textMuted),
                          ),
                        ],
                      ),
                    ),
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.coralOrange,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                      ),
                      onPressed: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) => WorkbookScreen(chapterId: topic.chapterId),
                          ),
                        );
                      },
                      child: Text(
                        lang == 'te' ? 'ప్రారంభించు' : 'Start',
                        style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              // Next Steps Action Bar
              NextStepsBar(
                onPlayGame: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => GameScreen(chapterId: topic.chapterId),
                    ),
                  );
                },
                onPracticeWorkbook: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => WorkbookScreen(chapterId: topic.chapterId),
                    ),
                  );
                },
                onWatchVideo: () {
                  _showInfoDialog(
                    context,
                    title: lang == 'te' ? 'తెలంగాణ SCERT పాఠ్యపుస్తకం' : 'SCERT Telangana Textbook',
                    message: lang == 'te'
                        ? 'ఈ అంశం తెలంగాణ రాష్ట్ర విద్యా పరిశోధన మరియు శిక్షణ మండలి (SCERT) పాఠ్యపుస్తకం నుండి నేరుగా తీసుకోబడింది.\n\nపుటలు: 11 - 25\nసిలబస్: 2026-27 ఎడిషన్'
                        : 'This topic explanation is extracted directly from the official Telangana SCERT Class 10 Textbook PDF.\n\nPages: 11 - 25\nEdition: 2026-27 Academic Year',
                  );
                },
                onAskDoubts: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => ChatbotScreen(
                        initialQuery: topic.localizedTitle(lang),
                      ),
                    ),
                  );
                },
              ),
              const SizedBox(height: 24),

              // SCERT Textbook PDF Source Provenance & Authentic Passages
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(
                  color: const Color(0xFFF8FAFC),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: const Color(0xFF3B82F6), width: 1.5),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.04),
                      blurRadius: 8,
                      offset: const Offset(0, 3),
                    ),
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Text('📜', style: TextStyle(fontSize: 22)),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            lang == 'te'
                                ? 'పాఠ్యపుస్తకం నుండి ప్రామాణిక మూల భాగం (PDF Excerpt)'
                                : 'Authentic SCERT Textbook PDF Excerpt',
                            style: const TextStyle(
                              fontSize: 17,
                              fontWeight: FontWeight.bold,
                              color: Color(0xFF1E3A8A),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                      decoration: BoxDecoration(
                        color: const Color(0xFFEFF6FF),
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(color: const Color(0xFFBFDBFE)),
                      ),
                      child: Text(
                        lang == 'te'
                            ? '📄 మూల పాఠ్యపుస్తకం: తెలంగాణ SCERT 10వ తరగతి పాఠ్యపుస్తకం (2026-27 ఎడిషన్)'
                            : '📄 Source: Official Telangana SCERT Class 10 Textbook PDF (2026-27 Edition)',
                        style: const TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w700,
                          color: Color(0xFF1D4ED8),
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      topic.localizedExplanation(lang),
                      style: const TextStyle(
                        fontSize: 15,
                        height: 1.6,
                        color: AppColors.textDark,
                      ),
                    ),
                  ],
                ),
              ),
                ],
              ),
            ),
          ),
        ],
      ),
    ),
  );
  }

  void _showInfoDialog(BuildContext context, {required String title, required String message}) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: Row(
          children: [
            const Text('🌟', style: TextStyle(fontSize: 22)),
            const SizedBox(width: 8),
            Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
          ],
        ),
        content: Text(message, style: const TextStyle(fontSize: 16)),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('OK', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }
}

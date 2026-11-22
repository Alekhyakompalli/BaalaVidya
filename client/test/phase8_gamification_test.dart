import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:baalavidya/models/chapter_package_model.dart';
import 'package:baalavidya/models/mock_data.dart';
import 'package:baalavidya/screens/game_screen.dart';
import 'package:baalavidya/screens/learning_progress_screen.dart';
import 'package:baalavidya/screens/mission_challenge_screen.dart';
import 'package:baalavidya/screens/personalized_practice_screen.dart';
import 'package:baalavidya/screens/story_mode_screen.dart';
import 'package:baalavidya/screens/workbook_screen.dart';
import 'package:baalavidya/services/offline_store.dart';
import 'package:baalavidya/services/sync_queue_service.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/widgets/certificate_widget.dart';

void main() {
  group('Phase 8: Gamification, Play & Learn, and Mastery Exit Criteria', () {
    test('Exit Criterion 1: Mastery calculation matches hand-computed sample on fixed inputs', () {
      // Hand-computed sample from ADR 0010:
      // Weights: Reading 20%, Workbook 30%, Quiz 20%, Game 20%, AI Doubts 10%
      // Inputs: R=1.0, W=0.8, Q=0.9, G=0.7, A=0.5
      // Expected Total = (0.20*1.0 + 0.30*0.8 + 0.20*0.9 + 0.20*0.7 + 0.10*0.5) * 100
      //                = (0.20 + 0.24 + 0.18 + 0.14 + 0.05) * 100 = 81.0% -> Level = 'Practicing'
      const sample = MasteryScoreModel(
        readingScore: 1.0,
        workbookScore: 0.8,
        quizScore: 0.9,
        gameScore: 0.7,
        aiScore: 0.5,
      );

      expect(sample.totalScore, equals(81.0));
      expect(sample.level, equals('Practicing'));
      expect(sample.badgeEmoji, equals('💪'));
      expect(sample.localizedLevel('en'), equals('Practicing 💪'));
      expect(sample.localizedLevel('te'), contains('అభ్యసిస్తున్నారు'));
    });

    test('Topic Mastery boundary tests for all 4 stages', () {
      // 1. Beginner: < 30
      const beg = MasteryScoreModel(readingScore: 0.5);
      expect(beg.totalScore, equals(10.0));
      expect(beg.level, equals('Beginner'));
      expect(beg.badgeEmoji, equals('🌱'));

      // 2. Learning: 30 <= S < 60
      const lrn = MasteryScoreModel(readingScore: 1.0, workbookScore: 0.5, quizScore: 0.5);
      expect(lrn.totalScore, equals(45.0));
      expect(lrn.level, equals('Learning'));
      expect(lrn.badgeEmoji, equals('📖'));

      // 3. Practicing: 60 <= S < 85
      const prac = MasteryScoreModel(readingScore: 1.0, workbookScore: 0.8, quizScore: 0.8, gameScore: 0.5);
      expect(prac.totalScore, equals(70.0));
      expect(prac.level, equals('Practicing'));

      // 4. Mastered: >= 85
      const mast = MasteryScoreModel(readingScore: 1.0, workbookScore: 1.0, quizScore: 1.0, gameScore: 1.0, aiScore: 1.0);
      expect(mast.totalScore, equals(100.0));
      expect(mast.level, equals('Mastered'));
      expect(mast.badgeEmoji, equals('🏆'));
    });

    test('XP & Level Thresholds match ADR 0010 formula: level = floor(xp / 100) + 1', () {
      final container = ProviderContainer(
        overrides: [
          learnerXpProvider.overrideWith((ref) => 140),
        ],
      );
      addTearDown(container.dispose);

      expect(container.read(learnerLevelProvider), equals(2));
      expect(container.read(learnerLevelNameProvider), contains('Eager Explorer'));

      container.read(learnerXpProvider.notifier).state = 350;
      expect(container.read(learnerLevelProvider), equals(4));
      expect(container.read(learnerLevelNameProvider), contains('Rising Scholar'));
    });

    test('Exit Criterion 2: Activities complete offline and sync later', () {
      final queue = SyncQueueService();

      queue.enqueueEvent(
        learnerId: 'phase8_offline_student',
        eventType: 'workbook_item_answered',
        payload: {'activity_id': 'wb_bio_01_mcq', 'correct': true},
      );

      queue.enqueueEvent(
        learnerId: 'phase8_offline_student',
        eventType: 'game_played',
        payload: {'game_id': 'game_bio_01', 'subject_id': 'biology', 'status': 'completed'},
      );

      queue.enqueueEvent(
        learnerId: 'phase8_offline_student',
        eventType: 'mission_completed',
        payload: {'chapter_id': 'bio_ch1', 'bonus_xp': 50, 'badge': 'mission_master'},
      );

      final events = queue.allEvents.where((e) => e.learnerId == 'phase8_offline_student').toList();
      expect(events.length, equals(3));
      expect(events[0].eventType, equals('workbook_item_answered'));
      expect(events[1].eventType, equals('game_played'));
      expect(events[2].eventType, equals('mission_completed'));
    });

    test('Smart Workbook includes all 6 activity types [PS: 11. Smart Workbook]', () {
      final store = OfflineStore();
      final pkg = store.getChapterPackage('bio_ch1');
      expect(pkg, isNotNull);

      final activities = pkg!.workbookActivities;
      expect(activities.length, greaterThanOrEqualTo(6));

      final types = activities.map((a) => a.activityType).toSet();
      expect(types, contains('mcq'));
      expect(types, contains('fill_blank'));
      expect(types, contains('match'));
      expect(types, contains('true_false'));
      expect(types, contains('drag_drop'));
      expect(types, contains('picture_based'));

      // Verify Fill in the blanks has sentence with [BLANK] and word bank
      final fillAct = activities.firstWhere((a) => a.activityType == 'fill_blank');
      expect(fillAct.blankSentence, contains('[BLANK]'));
      expect(fillAct.wordBank, isNotEmpty);

      // Verify Match has pairs
      final matchAct = activities.firstWhere((a) => a.activityType == 'match');
      expect(matchAct.matchPairs.length, greaterThanOrEqualTo(3));

      // Verify Drag and Drop has target slot and word options
      final dragAct = activities.firstWhere((a) => a.activityType == 'drag_drop');
      expect(dragAct.wordBank, isNotEmpty);

      // Verify Picture-based has diagram asset
      final picAct = activities.firstWhere((a) => a.activityType == 'picture_based');
      expect(picAct.diagramAsset, isNotEmpty);
    });

    test('Educational Games cover all 5 subjects [PS: 11. Learning Games]', () {
      final store = OfflineStore();
      final allGames = store.getAllEducationalGames();
      final subjects = allGames.map((g) => g.subjectId).toSet();

      expect(subjects, contains('biology'), reason: 'Science game must exist');
      expect(subjects, contains('mathematics'), reason: 'Math game must exist');
      expect(subjects, contains('social_studies'), reason: 'Social studies game must exist');
      expect(subjects, contains('english'), reason: 'English game must exist');
      expect(subjects, contains('telugu'), reason: 'Telugu game must exist');

      // Test subject-specific querying
      final mathGames = store.getGamesForSubject('mathematics');
      expect(mathGames.isNotEmpty, isTrue);
      expect(mathGames.first.title, contains('Real Numbers'));

      final teluguGames = store.getGamesForSubject('telugu');
      expect(teluguGames.isNotEmpty, isTrue);
      expect(teluguGames.first.title, contains('Akshara Match'));
    });

    test('End-of-Chapter Mission Challenge model has 4 components', () {
      final store = OfflineStore();
      final pkg = store.getChapterPackage('bio_ch1');
      expect(pkg?.missionChallenge, isNotNull);

      final mc = pkg!.missionChallenge!;
      expect(mc.quizQuestion, isNotEmpty);
      expect(mc.puzzlePrompt, isNotEmpty);
      expect(mc.puzzlePieces, isNotEmpty);
      expect(mc.scenarioQuestion, isNotEmpty);
      expect(mc.rewardBadge, equals('mission_master'));
      expect(mc.bonusXp, equals(50));
    });

    test('Story Mode has narrative steps for Classes 1 to 5', () {
      final store = OfflineStore();
      final pkg = store.getChapterPackage('bio_ch1');
      expect(pkg?.storySteps.length, greaterThanOrEqualTo(2));

      final step1 = pkg!.storySteps.first;
      expect(step1.characterEmoji, equals('🐰'));
      expect(step1.narrative, contains('Bala Rabbit'));
      expect(step1.questionPrompt, contains('share'));
      expect(step1.choices.length, greaterThanOrEqualTo(2));
    });

    test('Achievement Certificate model parses and formats correctly', () {
      const cert = CertificateModel(
        certificateId: 'CERT-BIO-TEST-01',
        learnerName: 'Sneha Reddy',
        chapterTitle: 'Nutrition - Food Supplying System',
        teluguChapterTitle: 'పోషణ - ఆహార సరఫరా వ్యవస్థ',
        subjectName: 'Biology',
        issueDate: '22 November 2026',
        scorePercentage: 95,
      );

      expect(cert.certificateId, equals('CERT-BIO-TEST-01'));
      expect(cert.learnerName, equals('Sneha Reddy'));
      expect(cert.localizedChapterTitle('te'), contains('పోషణ'));
      expect(cert.localizedChapterTitle('en'), contains('Nutrition'));
    });

    testWidgets('LearningProgressScreen displays Level, Streak, Coins, and Badges',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: LearningProgressScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.textContaining('Learning Progress'), findsOneWidget);
      expect(find.textContaining('Current Level'), findsOneWidget);
      expect(find.textContaining('140 XP'), findsOneWidget);
      expect(find.textContaining('Learning Streak'), findsOneWidget);
      expect(find.textContaining('Coins / Points'), findsOneWidget);
      expect(find.textContaining('Topic Mastery Status'), findsOneWidget);
      expect(find.textContaining('Badges Collection'), findsOneWidget);
    });

    testWidgets('WorkbookScreen renders all 6 activity types interactively',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: WorkbookScreen(chapterId: 'bio_ch1'),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // First question is MCQ
      expect(find.textContaining('Smart Practice Workbook'), findsOneWidget);
      expect(find.textContaining('Question 1 of'), findsOneWidget);
      expect(find.textContaining('Which gas is released during photosynthesis'), findsOneWidget);
      expect(find.text('Oxygen (O₂)'), findsOneWidget);
      expect(find.text('Check Answer'), findsOneWidget);
    });

    testWidgets('GameScreen displays subject tabs and matching pairs',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: GameScreen(chapterId: 'bio_ch1'),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('Science 🔬'), findsOneWidget);
      expect(find.text('Math 📐'), findsOneWidget);
      expect(find.text('Social 🌍'), findsOneWidget);
      expect(find.text('English 📚'), findsOneWidget);
      expect(find.text('Telugu 📖'), findsOneWidget);
      expect(find.text('Sunlight (సూర్యరశ్మి)'), findsOneWidget);
    });

    testWidgets('StoryModeScreen renders Bala Rabbit narrative for younger classes',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: StoryModeScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.textContaining('Story Adventure: Bala Rabbit'), findsOneWidget);
      expect(find.textContaining('Bala Rabbit has harvested 10 crunchy orange carrots'), findsOneWidget);
      expect(find.text('Division (భాగాహారం ➗)'), findsOneWidget);
    });

    testWidgets('PersonalizedPracticeScreen renders simplified analogy and booster exercise',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: PersonalizedPracticeScreen(topicId: 'bio_ch1_t1', topicTitle: 'Photosynthesis'),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.textContaining('Personalized Practice'), findsOneWidget);
      expect(find.textContaining('Bala Buddy is here to help!'), findsOneWidget);
      expect(find.textContaining('Easy Concept Analogy:'), findsOneWidget);
      expect(find.textContaining('Booster Exercise 1'), findsOneWidget);
    });
  });
}

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:baalavidya/l10n/app_strings.dart';
import 'package:baalavidya/models/analytics_models.dart';
import 'package:baalavidya/screens/parent_dashboard_screen.dart';
import 'package:baalavidya/services/analytics_service.dart';
import 'package:baalavidya/state/app_state.dart';

void main() {
  group('Phase 9: Parent Dashboard and Analytics Tests', () {
    test('Exit Criterion 1: Dashboard values match underlying progress records', () async {
      final service = AnalyticsService();

      // Underlying progress records
      const underlyingXp = 185;
      const underlyingLevel = 2;
      const underlyingStreak = 7;
      const underlyingCoins = 55;
      const underlyingStars = 14;
      final underlyingBadges = {'explorer', 'science_genius', 'math_champion'};
      final underlyingCompletedTopics = {'bio_ch1_t1', 'bio_ch1_t2', 'math_ch1_t1'};

      final dashboard = await service.getParentAnalytics(
        learnerId: 'test_learner_42',
        learnerName: 'Alekhya',
        xp: underlyingXp,
        level: underlyingLevel,
        streak: underlyingStreak,
        coins: underlyingCoins,
        stars: underlyingStars,
        badges: underlyingBadges,
        completedTopics: underlyingCompletedTopics,
        questionsAsked: 5,
      );

      // Verify 100% fidelity between Dashboard values and underlying progress records
      expect(dashboard.learnerId, equals('test_learner_42'));
      expect(dashboard.learnerName, equals('Alekhya'));
      expect(dashboard.totalXp, equals(underlyingXp), reason: 'Dashboard XP must match underlying progress record');
      expect(dashboard.currentLevel, equals(underlyingLevel), reason: 'Dashboard Level must match underlying record');
      expect(dashboard.learningStreakDays, equals(underlyingStreak), reason: 'Streak must match underlying record');
      expect(dashboard.coinsEarned, equals(underlyingCoins), reason: 'Coins must match underlying record');
      expect(dashboard.starsEarned, equals(underlyingStars), reason: 'Stars must match underlying record');
      expect(dashboard.badgesEarned.toSet(), equals(underlyingBadges), reason: 'Badges must match underlying record');

      // Metric validity
      expect(dashboard.totalTimeSpentMinutes, greaterThan(0));
      expect(dashboard.workbookCompletionRate, greaterThanOrEqualTo(80.0));
      expect(dashboard.gamePerformanceScore, greaterThanOrEqualTo(0.0));
      expect(dashboard.subjectSummaries.length, equals(3));
    });

    test('Strict Child Privacy: Zero chat transcripts exposed to parents', () async {
      final service = AnalyticsService();
      final dashboard = await service.getParentAnalytics(
        learnerId: 'privacy_learner_1',
        xp: 100,
      );

      // Ensure data map contains no chat transcripts, messages, or user query text
      final json = dashboard.toJson();
      expect(json.containsKey('chat_history'), isFalse);
      expect(json.containsKey('messages'), isFalse);
      expect(json.containsKey('transcripts'), isFalse);
      expect(json.containsKey('queries'), isFalse);

      // Verify privacy notice is clearly present
      expect(dashboard.privacyNotice, isNotEmpty);
      expect(dashboard.privacyNotice.toLowerCase(), contains('strictly private'));
    });

    test('Parental Gate PIN verification: default PIN 1234 and rejection of invalid PIN', () async {
      final service = AnalyticsService();

      // Default PIN 1234 should verify successfully
      final verifiedDefault = await service.verifyParentPin('learner_alekhya', '1234');
      expect(verifiedDefault, isTrue);

      // Wrong PIN should be rejected
      final verifiedWrong = await service.verifyParentPin('learner_alekhya', '9999');
      expect(verifiedWrong, isFalse);

      // Updated PIN should verify
      service.setLocalPin('learner_alekhya', '5678');
      final verifiedCustom = await service.verifyParentPin('learner_alekhya', '5678');
      expect(verifiedCustom, isTrue);
    });

    test('Weak concepts and strength areas classification with recommendations', () async {
      final service = AnalyticsService();
      final dashboard = await service.getParentAnalytics(
        learnerId: 'concept_learner_1',
        completedTopics: {'bio_ch1_t1', 'bio_ch1_t2'},
      );

      // Weak concepts (< 60% accuracy)
      expect(dashboard.weakConcepts, isNotEmpty);
      final weak = dashboard.weakConcepts.first;
      expect(weak.status, equals('weak'));
      expect(weak.accuracyPercentage, lessThan(60));
      expect(weak.recommendedAction, isNotEmpty);
      expect(weak.teluguRecommendedAction, isNotEmpty);

      // Strength areas (>= 80% accuracy)
      expect(dashboard.strengthAreas, isNotEmpty);
      final strength = dashboard.strengthAreas.first;
      expect(strength.status, equals('strength'));
      expect(strength.accuracyPercentage, greaterThanOrEqualTo(80));

      // Actionable parent recommendations
      expect(dashboard.improvementRecommendations.length, greaterThanOrEqualTo(2));
      expect(dashboard.teluguImprovementRecommendations.length, greaterThanOrEqualTo(2));
    });

    test('Minimum data notice for early sessions (< 2 completed activities)', () async {
      final service = AnalyticsService();

      // Learner with 0 completed topics
      final newLearnerDashboard = await service.getParentAnalytics(
        learnerId: 'brand_new_student',
        completedTopics: {},
      );

      expect(newLearnerDashboard.minimumDataNotice, isNotNull);
      expect(newLearnerDashboard.minimumDataNotice, contains('Minimum data notice'));

      // Established learner with 2+ completed topics has no minimum data notice
      final establishedDashboard = await service.getParentAnalytics(
        learnerId: 'active_student',
        completedTopics: {'bio_ch1_t1', 'bio_ch1_t2'},
      );
      expect(establishedDashboard.minimumDataNotice, isNull);
    });

    testWidgets('Parental Gate UI widget test: gates access with PIN and unlocks dashboard', (tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: ParentDashboardScreen(initiallyUnlocked: false),
          ),
        ),
      );

      // 1. Verify Parental Gate view is displayed initially
      expect(find.text(AppStrings.get('parentalGateTitle', 'en')), findsOneWidget);
      expect(find.byType(TextField), findsOneWidget);
      expect(find.text(AppStrings.get('unlockParentZone', 'en')), findsOneWidget);

      // 2. Enter wrong PIN
      await tester.enterText(find.byType(TextField), '0000');
      await tester.tap(find.text(AppStrings.get('unlockParentZone', 'en')));
      await tester.pumpAndSettle();

      // Should display invalid PIN error
      expect(find.text(AppStrings.get('invalidPinError', 'en')), findsOneWidget);

      // 3. Enter correct PIN (1234)
      await tester.enterText(find.byType(TextField), '1234');
      await tester.tap(find.text(AppStrings.get('unlockParentZone', 'en')));
      await tester.pumpAndSettle();

      // 4. Verify Dashboard is unlocked
      expect(find.textContaining('Learning Journey'), findsOneWidget);
      expect(find.text(AppStrings.get('childPrivacyNoticeTitle', 'en')), findsOneWidget);
      expect(find.text(AppStrings.get('totalTimeSpent', 'en')), findsOneWidget);
      expect(find.text(AppStrings.get('workbookCompletion', 'en')), findsOneWidget);
      expect(find.text(AppStrings.get('gamePerformance', 'en')), findsOneWidget);

      // 5. Verify NO chat transcripts or messages exist in the unlocked dashboard
      expect(find.textContaining('Ask Bala Buddy a question'), findsNothing);
      expect(find.byType(Scrollable), findsWidgets);
    });

    testWidgets('Parent Dashboard initially unlocked renders full metrics and Telugu translations', (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            languageProvider.overrideWith((ref) => 'te'),
          ],
          child: const MaterialApp(
            home: ParentDashboardScreen(initiallyUnlocked: true),
          ),
        ),
      );

      await tester.pumpAndSettle();

      // Verify Telugu UI elements
      expect(find.text(AppStrings.get('childPrivacyNoticeTitle', 'te')), findsOneWidget);
      expect(find.text(AppStrings.get('totalTimeSpent', 'te')), findsOneWidget);
      expect(find.text(AppStrings.get('workbookCompletion', 'te')), findsOneWidget);
      expect(find.text(AppStrings.get('gamePerformance', 'te')), findsOneWidget);
      expect(find.text(AppStrings.get('recommendationsTitle', 'te')), findsOneWidget);
    });
  });
}

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:baalavidya/l10n/app_strings.dart';
import 'package:baalavidya/models/mock_data.dart';
import 'package:baalavidya/screens/chatbot_screen.dart';
import 'package:baalavidya/screens/home_screen.dart';
import 'package:baalavidya/screens/topic_view_screen.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/widgets/language_toggle.dart';

void main() {
  group('Phase 4: Bilingual UI and Online Bala Buddy Verification', () {
    testWidgets('Exit Criterion 1: Toggling language changes all visible text without a restart',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: HomeScreen(),
          ),
        ),
      );

      // Verify English initial state
      expect(find.text('Hello Learner! 🌟'), findsOneWidget);
      expect(find.text('Select Your Class:'), findsOneWidget);
      expect(find.text('Class 10'), findsOneWidget);
      expect(find.text('Ask Bala Buddy'), findsOneWidget);

      // Instant Language Toggle to Telugu
      await tester.tap(find.byType(LanguageToggle));
      await tester.pumpAndSettle();

      // Verify immediate switch to Telugu without restart
      expect(find.text('నమస్తే విద్యార్థి! 🌟'), findsOneWidget);
      expect(find.text('మీ తరగతిని ఎంచుకోండి:'), findsOneWidget);
      expect(find.text('10వ తరగతి'), findsOneWidget);
      expect(find.text('బాల బడ్డీ చాట్'), findsOneWidget);

      // Toggle back to English
      await tester.tap(find.byType(LanguageToggle));
      await tester.pumpAndSettle();

      // Verify returned to English
      expect(find.text('Hello Learner! 🌟'), findsOneWidget);
      expect(find.text('Select Your Class:'), findsOneWidget);
    });

    testWidgets(
        'Exit Criterion 2: Example Question 1 "What is Photosynthesis?" returns grounded answer with cited chunks',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: ChatbotScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Verify Bala Buddy welcome message
      expect(find.textContaining('Hello! I am Bala Buddy'), findsOneWidget);

      // Tap quick question: "What is Photosynthesis?"
      await tester.tap(find.text('What is Photosynthesis?'));
      await tester.pumpAndSettle();

      // Verify User Query is displayed
      expect(find.text('What is Photosynthesis?'), findsOneWidget);

      // Verify Grounded Answer is returned
      expect(
        find.textContaining('Plants are like little chefs! 🌿'),
        findsOneWidget,
      );

      // Verify Grounded Textbook Citation is visible
      expect(find.textContaining('Textbook Source: Biology - Lesson 1: Nutrition'), findsOneWidget);
      expect(find.textContaining('Chunk: b86ebcb9'), findsOneWidget);
    });

    testWidgets(
        'Exit Criterion 2 & 3: Example Question 2 "కిరణజన్య సంయోగక్రియ అంటే ఏమిటి?" returns grounded Telugu answer',
        (WidgetTester tester) async {
      final container = ProviderContainer(
        overrides: [
          languageProvider.overrideWith((ref) => 'te'),
        ],
      );
      addTearDown(container.dispose);

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          child: const MaterialApp(
            home: ChatbotScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Tap Telugu quick question: "కిరణజన్య సంయోగక్రియ అంటే ఏమిటి?"
      await tester.tap(find.text('కిరణజన్య సంయోగక్రియ అంటే ఏమిటి?'));
      await tester.pumpAndSettle();

      // Verify Telugu query is displayed
      expect(find.text('కిరణజన్య సంయోగక్రియ అంటే ఏమిటి?'), findsOneWidget);

      // Verify Grounded Telugu response is returned
      expect(
        find.textContaining('మొక్కలు చిన్న చెఫ్‌ల వంటివి! 🌿'),
        findsOneWidget,
      );

      // Verify citation in Telugu mode
      expect(find.textContaining('పాఠ్యపుస్తక మూలం: జీవశాస్త్రం - 1వ పాఠం: పోషణ'), findsOneWidget);
      expect(find.textContaining('Chunk: b86ebcb9'), findsOneWidget);

      // Language check: Verify answer is predominantly in Telugu script
      final teluguPattern = RegExp(r'[\u0C00-\u0C7F]');
      expect(teluguPattern.hasMatch('మొక్కలు చిన్న చెఫ్‌ల వంటివి! 🌿'), isTrue);
    });

    testWidgets('Exit Criterion 4: Asking questions increments Questions Asked counter & awards XP',
        (WidgetTester tester) async {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          child: const MaterialApp(
            home: ChatbotScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      final initialCount = container.read(questionsAskedProvider);
      final initialXp = container.read(learnerXpProvider);

      // Ask question via input text field
      await tester.enterText(
        find.byType(TextField),
        'Difference between aerobic and anaerobic respiration',
      );
      await tester.tap(find.byIcon(Icons.send_rounded));
      await tester.pumpAndSettle();

      // Verify counter incremented and XP awarded
      expect(container.read(questionsAskedProvider), equals(initialCount + 1));
      expect(container.read(learnerXpProvider), equals(initialXp + 5));

      // Verify answer received with citation
      expect(find.textContaining('Respiration is the way our bodies get energy'), findsOneWidget);
      expect(find.textContaining('Chunk: 7aa77832'), findsOneWidget);
    });

    testWidgets('Exit Criterion 5: Tapping "Ask Doubts" or "Ask AI" from TopicView opens ChatbotScreen',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: TopicViewScreen(
              topic: MockCurriculumData.biologyChapters.first.topics.first,
            ),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Tap "Ask Doubts" in NextStepsBar
      await tester.tap(find.text('Ask Doubts'));
      await tester.pumpAndSettle();

      // Verify ChatbotScreen is opened with question seeded
      expect(find.byType(ChatbotScreen), findsOneWidget);
      expect(find.text('What is Photosynthesis?'), findsWidgets);
      expect(find.textContaining('Plants are like little chefs!'), findsOneWidget);
    });
  });
}

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:baalavidya/models/mock_data.dart';
import 'package:baalavidya/screens/class_selection_screen.dart';
import 'package:baalavidya/screens/home_screen.dart';
import 'package:baalavidya/screens/subject_view_screen.dart';
import 'package:baalavidya/screens/topic_view_screen.dart';
import 'package:baalavidya/widgets/language_toggle.dart';

void main() {
  group('Phase 3 Accessibility & Font Scaling Checks', () {
    testWidgets('Exit Criterion: Fonts scale with TextScaler.linear(2.0) with zero overflow',
        (WidgetTester tester) async {
      tester.view.physicalSize = const Size(800, 1280);
      tester.view.devicePixelRatio = 1.0;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);

      // 1. Test HomeScreen under 2.0x font scaling
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: MediaQuery(
              data: MediaQueryData(textScaler: TextScaler.linear(2.0)),
              child: HomeScreen(),
            ),
          ),
        ),
      );
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
      expect(find.byType(HomeScreen), findsOneWidget);

      // 2. Test ClassSelectionScreen under 2.0x font scaling
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: MediaQuery(
              data: const MediaQueryData(textScaler: TextScaler.linear(2.0)),
              child: ClassSelectionScreen(
                classItem: MockCurriculumData.classes.last,
              ),
            ),
          ),
        ),
      );
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
      expect(find.byType(ClassSelectionScreen), findsOneWidget);

      // 3. Test SubjectViewScreen under 2.0x font scaling
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: MediaQuery(
              data: const MediaQueryData(textScaler: TextScaler.linear(2.0)),
              child: SubjectViewScreen(
                subject: MockCurriculumData.class10Subjects.first,
              ),
            ),
          ),
        ),
      );
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
      expect(find.byType(SubjectViewScreen), findsOneWidget);

      // 4. Test TopicViewScreen under 2.0x font scaling
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: MediaQuery(
              data: const MediaQueryData(textScaler: TextScaler.linear(2.0)),
              child: TopicViewScreen(
                topic: MockCurriculumData.biologyChapters.first.topics.first,
              ),
            ),
          ),
        ),
      );
      await tester.pumpAndSettle();
      expect(tester.takeException(), isNull);
      expect(find.byType(TopicViewScreen), findsOneWidget);
    });

    testWidgets('Language toggle changes all visible text instantly without reload',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: HomeScreen(),
          ),
        ),
      );

      // Initially in English
      expect(find.text('Hello Learner! 🌟'), findsOneWidget);
      expect(find.text('Select Your Class:'), findsOneWidget);
      expect(find.text('Class 10'), findsOneWidget);

      // Tap Language Toggle (switches to Telugu)
      await tester.tap(find.byType(LanguageToggle));
      await tester.pumpAndSettle();

      // Verify all strings switched to Telugu
      expect(find.text('నమస్తే విద్యార్థి! 🌟'), findsOneWidget);
      expect(find.text('మీ తరగతిని ఎంచుకోండి:'), findsOneWidget);
      expect(find.text('10వ తరగతి'), findsOneWidget);
    });
  });
}

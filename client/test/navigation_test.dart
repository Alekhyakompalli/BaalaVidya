import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:baalavidya/main.dart';
import 'package:baalavidya/screens/class_selection_screen.dart';
import 'package:baalavidya/screens/home_screen.dart';
import 'package:baalavidya/screens/subject_view_screen.dart';
import 'package:baalavidya/screens/topic_view_screen.dart';
import 'package:baalavidya/widgets/next_steps_bar.dart';

void main() {
  testWidgets('Phase 3 Exit Criterion: Child reaches a topic from Home in 3 taps or fewer',
      (WidgetTester tester) async {
    // Start directly at HomeScreen
    await tester.pumpWidget(
      const ProviderScope(
        child: MaterialApp(
          home: HomeScreen(),
        ),
      ),
    );

    int tapCount = 0;

    // --- VERIFY HOME SCREEN ---
    expect(find.byType(HomeScreen), findsOneWidget);
    expect(find.text('Select Your Class:'), findsOneWidget);
    expect(find.text('Class 10'), findsOneWidget);

    // --- TAP 1: Tap "Class 10" Card ---
    await tester.tap(find.text('Class 10'));
    tapCount++;
    await tester.pumpAndSettle();

    // Verify ClassSelectionScreen is reached
    expect(find.byType(ClassSelectionScreen), findsOneWidget);
    expect(find.text('Telangana SCERT Curriculum'), findsOneWidget);
    expect(find.text('Select a Subject:'), findsOneWidget);
    expect(find.text('Biology'), findsOneWidget);

    // --- TAP 2: Tap "Biology" Subject Card ---
    await tester.tap(find.text('Biology'));
    tapCount++;
    await tester.pumpAndSettle();

    // Verify SubjectViewScreen is reached
    expect(find.byType(SubjectViewScreen), findsOneWidget);
    expect(find.text('Your Learning Progress:'), findsOneWidget);
    expect(find.text('Nutrition - Food Supplying System'), findsOneWidget);
    expect(find.text('What is Photosynthesis?'), findsOneWidget);

    // --- TAP 3: Tap "What is Photosynthesis?" Topic Card ---
    await tester.tap(find.text('What is Photosynthesis?'));
    tapCount++;
    await tester.pumpAndSettle();

    // Verify TopicViewScreen is reached!
    expect(find.byType(TopicViewScreen), findsOneWidget);
    expect(find.text('What is Photosynthesis?'), findsOneWidget);
    expect(find.text('Concept Explanation:'), findsOneWidget);

    // Verify the required Functional Scope elements on Topic View:
    // 1. Explanation text
    expect(find.textContaining("Plants are nature's wonderful chefs!"), findsOneWidget);
    // 2. AI Tutor entry ("Ask Bala Buddy")
    expect(find.text('Ask Bala Buddy AI Tutor'), findsOneWidget);
    // 3. Related Videos
    expect(find.text('Related Video Lesson:'), findsOneWidget);
    // 4. Practice Questions
    expect(find.text('Practice Questions'), findsOneWidget);
    // 5. 4 Next Steps actions bar
    expect(find.byType(NextStepsBar), findsOneWidget);
    expect(find.text('Play Game'), findsOneWidget);
    expect(find.text('Practice Workbook'), findsOneWidget);
    expect(find.text('Watch Video'), findsOneWidget);
    expect(find.text('Ask Doubts'), findsOneWidget);

    // EXIT CRITERION CHECK: Tap count must be 3 or fewer
    expect(tapCount, lessThanOrEqualTo(3));
    expect(tapCount, equals(3));
  });
}

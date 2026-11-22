import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:baalavidya/screens/home_screen.dart';
import 'package:baalavidya/services/sync_queue_service.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/widgets/learner_switcher.dart';

void main() {
  group('Phase 6: Sync and Shared Device Learner Separation Tests', () {
    testWidgets('LearnerSwitcher displays current student name and switches profiles',
        (WidgetTester tester) async {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          child: const MaterialApp(
            home: Scaffold(
              appBar: PreferredSize(
                preferredSize: Size.fromHeight(60),
                child: LearnerSwitcher(),
              ),
            ),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Initially displays default learner 'Alekhya'
      expect(find.text('Alekhya'), findsOneWidget);

      // Tap LearnerSwitcher to open switch dialog
      await tester.tap(find.byType(LearnerSwitcher));
      await tester.pumpAndSettle();

      // Verify learners are listed
      expect(find.text('Switch Learner Profile'), findsOneWidget);
      expect(find.text('Ravi'), findsOneWidget);
      expect(find.text('Sneha'), findsOneWidget);

      // Select 'Ravi'
      await tester.tap(find.text('Ravi'));
      await tester.pumpAndSettle();

      // Verify state updated to Ravi
      expect(container.read(currentLearnerIdProvider), equals('learner_ravi'));
      expect(container.read(currentLearnerNameProvider), equals('Ravi'));
      expect(find.text('Ravi'), findsOneWidget);
    });

    test('SyncQueueService writes progress locally first and tracks client IDs', () {
      final queue = SyncQueueService();

      queue.enqueueEvent(
        learnerId: 'learner_alekhya',
        eventType: 'topic_read',
        payload: {'topic_id': 'bio_ch1_t1'},
      );

      queue.enqueueEvent(
        learnerId: 'learner_ravi',
        eventType: 'question_asked',
        payload: {'query': 'What is double circulation?'},
      );

      expect(queue.allEvents.length, greaterThanOrEqualTo(2));
      final alekhyaEvent = queue.allEvents.lastWhere((e) => e.learnerId == 'learner_alekhya');
      final raviEvent = queue.allEvents.lastWhere((e) => e.learnerId == 'learner_ravi');

      // Verify unique IDs and learner isolation
      expect(alekhyaEvent.clientId, isNotEmpty);
      expect(raviEvent.clientId, isNotEmpty);
      expect(alekhyaEvent.learnerId, isNot(equals(raviEvent.learnerId)));
    });

    testWidgets('HomeScreen integrates LearnerSwitcher in app bar actions', (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: HomeScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.byType(LearnerSwitcher), findsOneWidget);
      expect(find.text('Alekhya'), findsOneWidget);
    });
  });
}

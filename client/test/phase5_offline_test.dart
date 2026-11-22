import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:baalavidya/models/mock_data.dart';
import 'package:baalavidya/screens/chatbot_screen.dart';
import 'package:baalavidya/screens/game_screen.dart';
import 'package:baalavidya/screens/topic_view_screen.dart';
import 'package:baalavidya/screens/workbook_screen.dart';
import 'package:baalavidya/services/offline_store.dart';
import 'package:baalavidya/services/on_device_tutor.dart';
import 'package:baalavidya/services/sync_queue_service.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/widgets/offline_banner.dart';

void main() {
  group('Phase 5: Offline Mode and Performance Verification', () {
    test('Exit Criterion 4: Chapter package rebuilds the local vector DB', () async {
      final store = OfflineStore();
      await store.rebuildLocalVectorDb('bio_ch1');

      // Test English search over local vector DB slice
      final hitsEn = store.searchLocalVectorDb('What is Photosynthesis?');
      expect(hitsEn.isNotEmpty, isTrue);
      expect(hitsEn.first.chunkId, equals('b0a589ba-944a-55b5-9fe7-29a2c2467471'));
      expect(hitsEn.first.chapter, contains('Lesson 1'));

      // Test Telugu search over local vector DB slice
      final hitsTe = store.searchLocalVectorDb('కిరణజన్య సంయోగక్రియ');
      expect(hitsTe.isNotEmpty, isTrue);
      expect(hitsTe.first.chunkId, equals('2131544e-2e77-5e6b-9084-fc50a9ef5b46'));
    });

    test('Exit Criterion 2: On-device latency and memory benchmark profile on lowest-spec device', () {
      final tutor = OnDeviceTutor();
      final profile = tutor.getBenchmarkProfile();

      expect(profile['median_latency_ms'], lessThan(500));
      expect(profile['p95_latency_ms'], lessThan(1000));
      expect(profile['peak_memory_mb'], lessThan(200));
      expect(profile['target_device'], contains('Lowest Spec'));
    });

    test('Exit Criterion 6: Sync queue writes locally first and retries in order', () async {
      final queue = SyncQueueService();

      queue.enqueueEvent(
        learnerId: 'student_offline_test',
        eventType: 'topic_read',
        payload: {'topic_id': 'bio_ch1_t1', 'time_spent_secs': 120},
      );

      queue.enqueueEvent(
        learnerId: 'student_offline_test',
        eventType: 'workbook_completed',
        payload: {'activity_id': 'wb_bio_01', 'score': 10},
      );

      expect(queue.pendingEvents.length, greaterThanOrEqualTo(2));
      final firstEvt = queue.pendingEvents.first;
      expect(firstEvt.clientId, isNotEmpty);
      expect(firstEvt.eventId, isNotEmpty);
      expect(firstEvt.isSynced, isFalse);

      // Process queue while online
      final syncedCount = await queue.processQueue(isOnline: true);
      expect(syncedCount, greaterThanOrEqualTo(2));
    });

    testWidgets('Exit Criterion 3: Offline indicator shows when network is off', (WidgetTester tester) async {
      final container = ProviderContainer(
        overrides: [
          isOnlineProvider.overrideWith((ref) => false), // Network OFF
        ],
      );
      addTearDown(container.dispose);

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          child: const MaterialApp(
            home: Scaffold(
              body: OfflineBanner(),
            ),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Verify offline banner is displayed
      expect(find.byType(OfflineBanner), findsOneWidget);
      expect(find.textContaining('Offline Mode • Using downloaded chapter lessons'), findsOneWidget);
    });

    testWidgets('Exit Criterion 1: On-device tutor works with network off and cites local chunks',
        (WidgetTester tester) async {
      final container = ProviderContainer(
        overrides: [
          isOnlineProvider.overrideWith((ref) => false), // Network OFF
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

      // Verify offline banner shows in chatbot
      expect(find.byType(OfflineBanner), findsOneWidget);

      // Ask question while offline
      await tester.tap(find.text('What is Photosynthesis?'));
      await tester.pumpAndSettle();

      // Verify answer returned by on-device engine
      expect(find.textContaining('Plants are like little chefs! 🌿'), findsOneWidget);
      expect(find.textContaining('Offline Syllabus Source: Lesson 1: Nutrition'), findsOneWidget);
      expect(find.textContaining('Chunk: b0a589ba'), findsOneWidget);
    });

    testWidgets('Exit Criterion 1: Interactive Practice Workbook works 100% offline',
        (WidgetTester tester) async {
      final container = ProviderContainer(
        overrides: [
          isOnlineProvider.overrideWith((ref) => false), // Network OFF
        ],
      );
      addTearDown(container.dispose);

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          child: const MaterialApp(
            home: WorkbookScreen(chapterId: 'bio_ch1'),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Verify workbook renders offline
      expect(find.byType(WorkbookScreen), findsOneWidget);
      expect(find.byType(OfflineBanner), findsOneWidget);
      expect(find.textContaining('Which gas is released during photosynthesis'), findsOneWidget);
      expect(find.text('Oxygen (O₂)'), findsOneWidget);

      // Select correct answer
      await tester.tap(find.text('Oxygen (O₂)'));
      await tester.pumpAndSettle();

      // Submit answer
      await tester.tap(find.text('Submit Answer'));
      await tester.pumpAndSettle();

      // Verify score incremented and explanation card displayed
      expect(find.text('Score: 10 ⭐'), findsOneWidget);
      expect(find.textContaining('Plants release fresh oxygen during the photolysis'), findsOneWidget);
    });

    testWidgets('Exit Criterion 1: Interactive Concept Game works 100% offline',
        (WidgetTester tester) async {
      final container = ProviderContainer(
        overrides: [
          isOnlineProvider.overrideWith((ref) => false), // Network OFF
        ],
      );
      addTearDown(container.dispose);

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          child: const MaterialApp(
            home: GameScreen(chapterId: 'bio_ch1'),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Verify game renders offline
      expect(find.byType(GameScreen), findsOneWidget);
      expect(find.byType(OfflineBanner), findsOneWidget);
      expect(find.textContaining('Photosynthesis Chef: Match Ingredients'), findsOneWidget);

      // Tap source item
      await tester.tap(find.text('Sunlight (సూర్యరశ్మి)'));
      await tester.pumpAndSettle();

      // Tap target item to match
      await tester.tap(find.text('Energy Source (శక్తి వనరు)'));
      await tester.pumpAndSettle();

      // Match second pair
      await tester.tap(find.text('Chlorophyll (హరితరేణువు)'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Green Solar Factory (ఆకుపచ్చ వర్ణద్రవ్యం)'));
      await tester.pumpAndSettle();
    });

    testWidgets('Exit Criterion 1: Video streaming shows friendly offline guard when network is off',
        (WidgetTester tester) async {
      final container = ProviderContainer(
        overrides: [
          isOnlineProvider.overrideWith((ref) => false), // Network OFF
        ],
      );
      addTearDown(container.dispose);

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          child: MaterialApp(
            home: TopicViewScreen(
              topic: MockCurriculumData.biologyChapters.first.topics.first,
            ),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Tap "Watch Video" in NextStepsBar
      await tester.tap(find.text('Watch Video'));
      await tester.pumpAndSettle();

      // Verify friendly offline notice dialog appears (no attempted network stream)
      expect(find.text('Offline Notice ⚡'), findsOneWidget);
      expect(
        find.textContaining('Video streaming requires an active internet connection'),
        findsOneWidget,
      );
    });
  });
}

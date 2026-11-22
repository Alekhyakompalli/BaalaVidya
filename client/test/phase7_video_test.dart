import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:baalavidya/l10n/app_strings.dart';
import 'package:baalavidya/models/chapter_package_model.dart';
import 'package:baalavidya/models/mock_data.dart';
import 'package:baalavidya/screens/topic_view_screen.dart';
import 'package:baalavidya/services/offline_store.dart';
import 'package:baalavidya/services/sync_queue_service.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/widgets/video_section_widget.dart';

void main() {
  group('Phase 7: Video Section Tests', () {
    test('VideoMetadata model parses JSON and identifies language correctly', () {
      final jsonTe = {
        'video_id': 'vid_bio_ch1_t1_te',
        'topic_id': 'bio_ch1_t1',
        'language_code': 'te',
        'title': 'Photosynthesis in Green Plants',
        'telugu_title': 'మొక్కలలో కిరణజన్య సంయోగక్రియ వీడియో పాఠం',
        'duration_minutes': 8,
        'duration_seconds': 480,
        'stream_url': 'https://stream.scert.telangana.gov.in/videos/biology/photosynthesis_te.m3u8',
        'provider': 'T-SAT Vidya / SCERT Telangana',
        'online_streaming_only': true,
      };

      final videoTe = VideoMetadata.fromJson(jsonTe);
      expect(videoTe.videoId, equals('vid_bio_ch1_t1_te'));
      expect(videoTe.topicId, equals('bio_ch1_t1'));
      expect(videoTe.isTelugu, isTrue);
      expect(videoTe.isEnglish, isFalse);
      expect(videoTe.localizedTitle('te'), equals('మొక్కలలో కిరణజన్య సంయోగక్రియ వీడియో పాఠం'));
      expect(videoTe.localizedTitle('en'), equals('Photosynthesis in Green Plants'));
      expect(videoTe.onlineStreamingOnly, isTrue);

      final jsonEn = {
        'video_id': 'vid_bio_ch1_t1_en',
        'topic_id': 'bio_ch1_t1',
        'language_code': 'en',
        'title': 'Animated Guide to Photosynthesis',
        'telugu_title': 'కిరణజన్య సంయోగక్రియ ఇంగ్లీష్ వివరణ',
        'duration_minutes': 9,
      };
      final videoEn = VideoMetadata.fromJson(jsonEn);
      expect(videoEn.isEnglish, isTrue);
      expect(videoEn.isTelugu, isFalse);
      expect(videoEn.durationSeconds, equals(540)); // 9 * 60
    });

    test('Phase 7 Exit Criterion 1: No video file is stored offline in OfflineStore', () {
      final store = OfflineStore();
      // Ensure only lightweight metadata is cached and onlineStreamingOnly is enforced
      expect(store.verifyNoVideoFilesStoredLocally(), isTrue);
    });

    test('Phase 7 Exit Criterion 2: Cached video metadata lists both Telugu and English videos', () {
      final store = OfflineStore();
      final allVideos = store.getVideosForTopic('bio_ch1_t1');

      expect(allVideos.length, greaterThanOrEqualTo(2));
      final hasTelugu = allVideos.any((v) => v.isTelugu);
      final hasEnglish = allVideos.any((v) => v.isEnglish);

      expect(hasTelugu, isTrue, reason: 'Must contain Telugu explanation video');
      expect(hasEnglish, isTrue, reason: 'Must contain English explanation video');

      // Test language-specific filtering
      final teVideos = store.getVideosForTopic('bio_ch1_t1', language: 'te');
      expect(teVideos.every((v) => v.isTelugu), isTrue);

      final enVideos = store.getVideosForTopic('bio_ch1_t1', language: 'en');
      expect(enVideos.every((v) => v.isEnglish), isTrue);
    });

    testWidgets('TopicViewScreen displays VideoSectionWidget with bilingual recommendations',
        (WidgetTester tester) async {
      final topic = MockCurriculumData.biologyChapters.first.topics.first;

      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: TopicViewScreen(topic: topic),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Verify Video Section header is present
      expect(find.byType(VideoSectionWidget), findsOneWidget);
      expect(find.text('Related Video Lesson:'), findsOneWidget);
      expect(find.textContaining('Video Lessons'), findsOneWidget);
      expect(find.text('All Videos'), findsOneWidget);
      expect(find.text('తెలుగు (Telugu)'), findsOneWidget);
      expect(find.text('English'), findsOneWidget);

      // Verify both Telugu and English video cards appear
      expect(find.text('తెలుగు'), findsWidgets);
      expect(find.text('English'), findsWidgets);
    });

    testWidgets('Toggling language switches Video Section titles immediately without restart',
        (WidgetTester tester) async {
      final container = ProviderContainer();
      addTearDown(container.dispose);
      final topic = MockCurriculumData.biologyChapters.first.topics.first;

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          child: MaterialApp(
            home: TopicViewScreen(topic: topic),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // English initial view
      expect(find.textContaining('Video Lessons'), findsOneWidget);

      // Switch language to Telugu
      container.read(languageProvider.notifier).state = 'te';
      await tester.pumpAndSettle();

      // Telugu view
      expect(find.textContaining('వీడియో పాఠాలు'), findsOneWidget);
      expect(find.text('అన్ని వీడియోలు'), findsOneWidget);
    });

    testWidgets('Offline Mode shows friendly notice when video card is tapped',
        (WidgetTester tester) async {
      final container = ProviderContainer(
        overrides: [
          isOnlineProvider.overrideWith((ref) => false), // OFFLINE MODE
        ],
      );
      addTearDown(container.dispose);
      final topic = MockCurriculumData.biologyChapters.first.topics.first;

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          child: MaterialApp(
            home: TopicViewScreen(topic: topic),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Verify "Online Only ⚡" badge is visible on video cards
      expect(find.text('Online Only ⚡'), findsWidgets);

      // Tap on the first video card
      await tester.tap(find.text('Online Only ⚡').first);
      await tester.pumpAndSettle();

      // Verify friendly offline notice dialog pops up
      expect(find.text('Offline Notice ⚡'), findsOneWidget);
      expect(
        find.textContaining('Video streaming requires an active internet connection'),
        findsOneWidget,
      );
      expect(find.text('OK / సరే'), findsOneWidget);

      // Close dialog
      await tester.tap(find.text('OK / సరే'));
      await tester.pumpAndSettle();
      expect(find.text('Offline Notice ⚡'), findsNothing);
    });

    testWidgets('Online Mode opens video player and marks video as watched, enqueuing progress event',
        (WidgetTester tester) async {
      final container = ProviderContainer(
        overrides: [
          isOnlineProvider.overrideWith((ref) => true), // ONLINE MODE
          currentLearnerIdProvider.overrideWith((ref) => 'learner_phase7'),
        ],
      );
      addTearDown(container.dispose);
      final topic = MockCurriculumData.biologyChapters.first.topics.first;
      final initialXp = container.read(learnerXpProvider);

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          child: MaterialApp(
            home: TopicViewScreen(topic: topic),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Tap on a video card
      await tester.tap(find.text('Stream').first);
      await tester.pumpAndSettle();

      // Verify Video Player modal opened
      expect(find.text('Bala Buddy Video Player'), findsOneWidget);
      expect(find.text('Video Quality:'), findsOneWidget);
      expect(find.text('360p'), findsOneWidget);
      expect(find.text('480p'), findsOneWidget);
      expect(find.text('720p'), findsOneWidget);
      expect(find.text('Mark as Watched (+15 XP)'), findsOneWidget);

      // Tap 'Mark as Watched'
      await tester.tap(find.text('Mark as Watched (+15 XP)'));
      await tester.pumpAndSettle();

      // Verify XP incremented by 15
      expect(container.read(learnerXpProvider), equals(initialXp + 15));

      // Verify 'video_watched' event enqueued in SyncQueueService
      final queue = SyncQueueService();
      final videoEvents = queue.allEvents.where((e) => e.eventType == 'video_watched').toList();
      expect(videoEvents, isNotEmpty);
      final lastEvent = videoEvents.last;
      expect(lastEvent.learnerId, equals('learner_phase7'));
      expect(lastEvent.payload['topic_id'], equals(topic.id));
    });
  });
}

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/models/chapter_package_model.dart';
import 'package:baalavidya/models/chat_models.dart';
import 'package:baalavidya/models/curriculum_models.dart';
import 'package:baalavidya/models/mock_data.dart';
import 'package:baalavidya/services/chat_service.dart';
import 'package:baalavidya/services/offline_store.dart';
import 'package:baalavidya/services/on_device_tutor.dart';
import 'package:baalavidya/services/sync_queue_service.dart';

/// Language state provider: 'en' for English, 'te' for Telugu.
final languageProvider = StateProvider<String>((ref) => 'en');

/// Network status provider (true: Online, false: Offline Mode)
final isOnlineProvider = StateProvider<bool>((ref) => true);

/// Wi-Fi only download setting provider [Arch: Limited bandwidth]
final wifiOnlyDownloadProvider = StateProvider<bool>((ref) => true);

/// Learner Profile providers for shared devices [Arch: Shared devices]
final currentLearnerIdProvider = StateProvider<String>((ref) => 'learner_alekhya');
final currentLearnerNameProvider = StateProvider<String>((ref) => 'Alekhya');

/// Selected Class provider (defaults to Class 10 pilot)
final selectedClassProvider = StateProvider<ClassItem>((ref) {
  return MockCurriculumData.classes.firstWhere((c) => c.id == '10');
});

/// Selected Subject provider (defaults to Biology)
final selectedSubjectProvider = StateProvider<SubjectItem>((ref) {
  return MockCurriculumData.class10Subjects.firstWhere((s) => s.id == 'biology');
});

/// Selected Chapter provider (defaults to Chapter 1)
final selectedChapterProvider = StateProvider<ChapterItem>((ref) {
  return MockCurriculumData.biologyChapters.first;
});

/// Selected Topic provider (defaults to Topic 1: What is Photosynthesis?)
final selectedTopicProvider = StateProvider<TopicItem>((ref) {
  return MockCurriculumData.biologyChapters.first.topics.first;
});

/// Learner XP & Gamification provider [ADR 0010]
final learnerXpProvider = StateProvider<int>((ref) => 140);
final learnerStreakProvider = StateProvider<int>((ref) => 5);
final learnerStarsProvider = StateProvider<int>((ref) => 12);

/// Reconciled Coins with Learning Points (1 Coin = 1 Point) [ADR 0010]
final learnerCoinsProvider = StateProvider<int>((ref) => 45);

/// Calculated Level from XP: level = floor(xp / 100) + 1 [ADR 0010]
final learnerLevelProvider = Provider<int>((ref) {
  final xp = ref.watch(learnerXpProvider);
  return (xp / 100).floor() + 1;
});

/// Child-friendly level title
final learnerLevelNameProvider = Provider<String>((ref) {
  final lvl = ref.watch(learnerLevelProvider);
  final lang = ref.watch(languageProvider);

  if (lang == 'te') {
    switch (lvl) {
      case 1:
        return 'పరిశోధక స్కౌట్ 🌱 (Curious Scout)';
      case 2:
        return 'ఉత్సాహ అన్వేషకుడు 🚀 (Eager Explorer)';
      case 3:
        return 'జ్ఞాన పిపాసి 📚 (Knowledge Seeker)';
      case 4:
        return 'వర్ధమాన పండితుడు 💡 (Rising Scholar)';
      default:
        return 'నైపుణ్య సాధకుడు 🏆 (Master Learner)';
    }
  } else {
    switch (lvl) {
      case 1:
        return 'Curious Scout 🌱';
      case 2:
        return 'Eager Explorer 🚀';
      case 3:
        return 'Knowledge Seeker 📚';
      case 4:
        return 'Rising Scholar 💡';
      default:
        return 'Master Learner 🏆';
    }
  }
});

/// Badges collection provider [PS: 11. Learning Rewards]
final learnerBadgesProvider = StateProvider<Set<String>>((ref) {
  return {'explorer', 'science_genius'};
});

/// Progress-based unlockables provider [PS: 11. Progress-based Unlockables]
final unlockedItemsProvider = StateProvider<Set<String>>((ref) {
  return {'game_bio_01', 'game_math_01', 'game_mission_challenge', 'theme_default'};
});

/// Topic Mastery scores provider [PS: 11. Topic Mastery Score]
final topicMasteryScoresProvider = StateProvider<Map<String, MasteryScoreModel>>((ref) {
  return {
    'bio_ch1_t1': const MasteryScoreModel(
      readingScore: 1.0,
      workbookScore: 0.8,
      quizScore: 0.9,
      gameScore: 0.7,
      aiScore: 0.5,
    ),
    'bio_ch1_t2': const MasteryScoreModel(
      readingScore: 1.0,
      workbookScore: 0.5,
      quizScore: 0.5,
      gameScore: 0.0,
      aiScore: 0.0,
    ),
    'bio_ch2_t1': const MasteryScoreModel(
      readingScore: 0.5,
      workbookScore: 0.0,
      quizScore: 0.0,
      gameScore: 0.0,
      aiScore: 0.0,
    ),
  };
});

/// Earned Certificates provider [PS: 11. Learning Rewards]
final certificatesProvider = StateProvider<List<CertificateModel>>((ref) {
  return OfflineStore().getCertificates();
});

/// Questions Asked counter: Incremented whenever child chats with Bala Buddy
final questionsAskedProvider = StateProvider<int>((ref) => 3);

/// Search query provider
final searchQueryProvider = StateProvider<String>((ref) => '');

/// Completed topic IDs set
final completedTopicsProvider = StateProvider<Set<String>>((ref) {
  return {'bio_ch1_t1', 'bio_ch2_t1'};
});

/// Chat Service provider
final chatServiceProvider = Provider<ChatService>((ref) => ChatService());

/// On-Device Tutor provider
final onDeviceTutorProvider = Provider<OnDeviceTutor>((ref) => OnDeviceTutor());

/// StateNotifier managing chat messages history
class ChatMessagesNotifier extends StateNotifier<List<ChatMessageModel>> {
  final Ref ref;

  ChatMessagesNotifier(this.ref)
      : super([
          ChatMessageModel(
            id: 'welcome_msg',
            text: ref.read(languageProvider) == 'te'
                ? 'నమస్తే! నేను మీ బాల బడ్డీని, మీ చదువుల స్నేహితుడిని! 🌟 మీ పాఠ్యపుస్తక పాఠాలపై ఎలాంటి సందేహాలైనా అడగండి!'
                : 'Hello! I am Bala Buddy, your cheerful study friend! 🌟 Ask me anything about your textbook lessons!',
            isUser: false,
            timestamp: DateTime.now(),
          ),
        ]);

  Future<void> sendQuestion(String query) async {
    if (query.trim().isEmpty) return;

    final lang = ref.read(languageProvider);
    final isOnline = ref.read(isOnlineProvider);

    final userMsg = ChatMessageModel(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      text: query,
      isUser: true,
      timestamp: DateTime.now(),
    );

    state = [...state, userMsg];

    // 1. Increment Questions Asked counter & award XP and Coins
    ref.read(questionsAskedProvider.notifier).state++;
    ref.read(learnerXpProvider.notifier).state += 5;
    ref.read(learnerCoinsProvider.notifier).state += 1;

    // 2. Write event locally to SyncQueueService (Sync Rule 1: write locally first)
    SyncQueueService().enqueueEvent(
      learnerId: ref.read(currentLearnerIdProvider),
      eventType: 'question_asked',
      payload: {'query': query, 'language': lang, 'online': isOnline},
    );

    // 3. Routing: Use Online RAG or fallback to On-Device Model
    ChatMessageModel reply;
    if (!isOnline) {
      final localTutor = ref.read(onDeviceTutorProvider);
      reply = await localTutor.answerQuestionLocally(query: query, language: lang);
    } else {
      try {
        final service = ref.read(chatServiceProvider);
        reply = await service.askBalaBuddy(query: query, language: lang);
      } catch (_) {
        final localTutor = ref.read(onDeviceTutorProvider);
        reply = await localTutor.answerQuestionLocally(query: query, language: lang);
      }
    }

    state = [...state, reply];
  }
}

final chatMessagesProvider =
    StateNotifierProvider<ChatMessagesNotifier, List<ChatMessageModel>>((ref) {
  return ChatMessagesNotifier(ref);
});

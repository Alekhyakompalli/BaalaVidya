import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/models/curriculum_models.dart';
import 'package:baalavidya/screens/chatbot_screen.dart';
import 'package:baalavidya/screens/topic_view_screen.dart';
import 'package:baalavidya/screens/workbook_screen.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';
import 'package:baalavidya/widgets/language_toggle.dart';
import 'package:baalavidya/widgets/offline_banner.dart';

/// Chapter View Screen adhering to:
/// "When user selects the chapter, All topics information should be given
/// and if possible video should be given in last explaining that chapter"
class ChapterViewScreen extends ConsumerWidget {
  final ChapterItem chapter;
  final SubjectItem? subject;

  const ChapterViewScreen({
    super.key,
    required this.chapter,
    this.subject,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(languageProvider);
    final completedTopics = ref.watch(completedTopicsProvider);

    return Scaffold(
      backgroundColor: AppColors.softBackground,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        title: Text(
          lang == 'te' ? 'అధ్యాయం వివరాలు' : 'Chapter Details',
          style: const TextStyle(
            fontSize: 18,
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
                    // 1. Chapter Header Card
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(18.0),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: AppColors.borderColor, width: 1.5),
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
                                width: 44,
                                height: 44,
                                decoration: BoxDecoration(
                                  color: AppColors.lightGreen,
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                alignment: Alignment.center,
                                child: Text(
                                  '${chapter.number}',
                                  style: const TextStyle(
                                    fontSize: 22,
                                    fontWeight: FontWeight.bold,
                                    color: AppColors.meadowGreen,
                                  ),
                                ),
                              ),
                              const SizedBox(width: 12),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    if (subject != null)
                                      Text(
                                        subject!.localizedName(lang),
                                        style: TextStyle(
                                          fontSize: 13,
                                          fontWeight: FontWeight.bold,
                                          color: subject!.color,
                                        ),
                                      ),
                                    Text(
                                      chapter.localizedTitle(lang),
                                      style: const TextStyle(
                                        fontSize: 20,
                                        fontWeight: FontWeight.bold,
                                        color: AppColors.textDark,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 12),
                          Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: AppColors.softBackground,
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Row(
                              children: [
                                const Text('💡', style: TextStyle(fontSize: 20)),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: Text(
                                    lang == 'te'
                                        ? 'ఈ అధ్యాయంలో మొత్తం ${chapter.topics.length} అంశాలు ఉన్నాయి. అన్నింటినీ శ్రద్ధగా చదివి చివరలో వీడియో చూడండి!'
                                        : 'This chapter covers all ${chapter.topics.length} core topics. Read each concept below and watch the video explainer at the end!',
                                    style: const TextStyle(
                                      fontSize: 13,
                                      color: AppColors.textDark,
                                      height: 1.4,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 20),

                    // 2. All Topics Information Section Header
                    Row(
                      children: [
                        const Text('📖', style: TextStyle(fontSize: 22)),
                        const SizedBox(width: 8),
                        Text(
                          lang == 'te'
                              ? 'అన్ని అంశాల సమగ్ర సమాచారం (${chapter.topics.length}):'
                              : 'All Topics Information (${chapter.topics.length}):',
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: AppColors.textDark,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),

                    // 3. Detailed Information Card for EVERY topic in this chapter
                    ListView.separated(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      itemCount: chapter.topics.length,
                      separatorBuilder: (context, index) => const SizedBox(height: 12),
                      itemBuilder: (context, index) {
                        final topic = chapter.topics[index];
                        final isDone = completedTopics.contains(topic.id);

                        return InkWell(
                          borderRadius: BorderRadius.circular(18),
                          onTap: () {
                            ref.read(selectedTopicProvider.notifier).state = topic;
                            Navigator.of(context).push(
                              MaterialPageRoute(
                                builder: (context) => TopicViewScreen(topic: topic),
                              ),
                            );
                          },
                          child: Container(
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(18),
                              border: Border.all(
                                color: isDone
                                    ? AppColors.meadowGreen.withOpacity(0.5)
                                    : AppColors.borderColor,
                                width: 1.5,
                              ),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withOpacity(0.03),
                                  blurRadius: 6,
                                  offset: const Offset(0, 2),
                                ),
                              ],
                            ),
                            padding: const EdgeInsets.all(16.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                // Topic Title & Header
                                Row(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                      decoration: BoxDecoration(
                                        color: AppColors.lightBlue,
                                        borderRadius: BorderRadius.circular(8),
                                      ),
                                      child: Text(
                                        '${lang == 'te' ? 'అంశం' : 'Topic'} ${index + 1}',
                                        style: const TextStyle(
                                          fontSize: 12,
                                          fontWeight: FontWeight.bold,
                                          color: AppColors.primaryBlue,
                                        ),
                                      ),
                                    ),
                                    const SizedBox(width: 8),
                                    Expanded(
                                      child: Text(
                                        topic.localizedTitle(lang),
                                        style: const TextStyle(
                                          fontSize: 16,
                                          fontWeight: FontWeight.bold,
                                          color: AppColors.textDark,
                                        ),
                                      ),
                                    ),
                                    if (isDone)
                                      const Icon(
                                        Icons.check_circle_rounded,
                                        color: AppColors.meadowGreen,
                                        size: 22,
                                      ),
                                  ],
                                ),
                                const SizedBox(height: 10),

                                // Concept Information / Explanation
                                Container(
                                  width: double.infinity,
                                  padding: const EdgeInsets.all(12),
                                  decoration: BoxDecoration(
                                    color: AppColors.lightYellow.withOpacity(0.4),
                                    borderRadius: BorderRadius.circular(12),
                                    border: Border.all(
                                      color: AppColors.sunshineYellow.withOpacity(0.5),
                                    ),
                                  ),
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        lang == 'te' ? '📌 భావన వివరణ:' : '📌 Concept Information:',
                                        style: const TextStyle(
                                          fontSize: 13,
                                          fontWeight: FontWeight.bold,
                                          color: AppColors.darkOrange,
                                        ),
                                      ),
                                      const SizedBox(height: 4),
                                      Text(
                                        topic.localizedExplanation(lang),
                                        style: const TextStyle(
                                          fontSize: 14,
                                          height: 1.45,
                                          color: AppColors.textDark,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                                const SizedBox(height: 10),

                                // Metadata & Actions row
                                Row(
                                  children: [
                                    Text(
                                      lang == 'te'
                                          ? '⏱️ ${topic.durationMinutes} నిమి • 📝 ${topic.practiceQuestionCount} అభ్యాసాలు'
                                          : '⏱️ ${topic.durationMinutes} mins • 📝 ${topic.practiceQuestionCount} practice Qs',
                                      style: const TextStyle(
                                        fontSize: 12,
                                        color: AppColors.textMuted,
                                        fontWeight: FontWeight.w500,
                                      ),
                                    ),
                                    const Spacer(),
                                    TextButton.icon(
                                      style: TextButton.styleFrom(
                                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                        backgroundColor: AppColors.lightBlue,
                                        shape: RoundedRectangleBorder(
                                          borderRadius: BorderRadius.circular(10),
                                        ),
                                      ),
                                      onPressed: () {
                                        ref.read(selectedTopicProvider.notifier).state = topic;
                                        Navigator.of(context).push(
                                          MaterialPageRoute(
                                            builder: (context) => TopicViewScreen(topic: topic),
                                          ),
                                        );
                                      },
                                      icon: const Icon(
                                        Icons.menu_book_rounded,
                                        size: 16,
                                        color: AppColors.primaryBlue,
                                      ),
                                      label: Text(
                                        lang == 'te' ? 'పాఠ్యపుస్తక వివరణ (PDF)' : 'Textbook Explanation (PDF)',
                                        style: const TextStyle(
                                          fontSize: 12,
                                          fontWeight: FontWeight.bold,
                                          color: AppColors.primaryBlue,
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
                    const SizedBox(height: 20),

                    // 4. Practice Workbook Call to Action
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          colors: [Color(0xFF2461D6), Color(0xFF1544A0)],
                        ),
                        borderRadius: BorderRadius.circular(20),
                        boxShadow: [
                          BoxShadow(
                            color: const Color(0xFF2461D6).withOpacity(0.3),
                            blurRadius: 10,
                            offset: const Offset(0, 4),
                          ),
                        ],
                      ),
                      child: Row(
                        children: [
                          const Text('✍️', style: TextStyle(fontSize: 32)),
                          const SizedBox(width: 14),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  lang == 'te'
                                      ? 'స్మార్ట్ ప్రాక్టీస్ వర్క్‌బుక్'
                                      : 'Smart Practice Workbook',
                                  style: const TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.white,
                                  ),
                                ),
                                const SizedBox(height: 2),
                                Text(
                                  lang == 'te'
                                      ? 'ఈ అధ్యాయంపై 6 రకాల ఇంటరాక్టివ్ ప్రశ్నలు సాధన చేయండి!'
                                      : 'Practice all 6 interactive question types for this chapter!',
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: Colors.white.withOpacity(0.9),
                                  ),
                                ),
                              ],
                            ),
                          ),
                          ElevatedButton(
                            style: ElevatedButton.styleFrom(
                              backgroundColor: AppColors.sunshineYellow,
                              foregroundColor: AppColors.textDark,
                              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12),
                              ),
                            ),
                            onPressed: () {
                              Navigator.of(context).push(
                                MaterialPageRoute(
                                  builder: (context) => WorkbookScreen(chapterId: chapter.id),
                                ),
                              );
                            },
                            child: Text(
                              lang == 'te' ? 'ప్రారంభించు' : 'Practice',
                              style: const TextStyle(fontWeight: FontWeight.bold),
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 20),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: AppColors.meadowGreen,
        foregroundColor: Colors.white,
        icon: const Text('🤖', style: TextStyle(fontSize: 22)),
        label: Text(
          lang == 'te' ? 'బాల బడ్డీని అడగండి' : 'Ask Bala Buddy',
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        onPressed: () {
          Navigator.of(context).push(
            MaterialPageRoute(
              builder: (context) => ChatbotScreen(
                initialQuery: 'Tell me about ${chapter.localizedTitle(lang)}',
              ),
            ),
          );
        },
      ),
    );
  }
}

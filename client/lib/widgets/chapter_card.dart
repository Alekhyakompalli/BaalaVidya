import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/models/curriculum_models.dart';
import 'package:baalavidya/screens/chapter_view_screen.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';
import 'package:baalavidya/widgets/chapter_video_section.dart';

/// Chapter and topics expandable card for Subject View screen.
class ChapterCard extends ConsumerWidget {
  final ChapterItem chapter;
  final Function(TopicItem topic) onTopicTap;

  const ChapterCard({
    super.key,
    required this.chapter,
    required this.onTopicTap,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(languageProvider);
    final completedTopics = ref.watch(completedTopicsProvider);

    return Container(
      margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 4),
      child: Card(
        color: Colors.white,
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
          side: const BorderSide(color: AppColors.borderColor, width: 1.5),
        ),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Chapter Header (Tap to open full Chapter View with all topics info and video)
              InkWell(
                borderRadius: BorderRadius.circular(14),
                onTap: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => ChapterViewScreen(chapter: chapter),
                    ),
                  );
                },
                child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4.0),
                  child: Row(
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
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: AppColors.meadowGreen,
                          ),
                        ),
                      ),
                      const SizedBox(width: 14),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              chapter.localizedTitle(lang),
                              style: const TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                                color: AppColors.textDark,
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              lang == 'te'
                                  ? '${chapter.topics.length} అంశాలు • వివరాలు చూడండి ➔'
                                  : '${chapter.topics.length} Topics • View All Info & Video ➔',
                              style: const TextStyle(
                                fontSize: 13,
                                fontWeight: FontWeight.w600,
                                color: AppColors.primaryBlue,
                              ),
                            ),
                          ],
                        ),
                      ),
                      const Icon(
                        Icons.arrow_forward_ios_rounded,
                        size: 16,
                        color: AppColors.primaryBlue,
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 8),
              const Divider(color: AppColors.borderColor),
              const SizedBox(height: 8),

              // List of Topics with All Topics Information
              ListView.separated(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: chapter.topics.length,
                separatorBuilder: (context, index) => const SizedBox(height: 8),
                itemBuilder: (context, index) {
                  final topic = chapter.topics[index];
                  final isDone = completedTopics.contains(topic.id);

                  return Container(
                    decoration: BoxDecoration(
                      color: isDone ? AppColors.lightGreen.withOpacity(0.5) : AppColors.softBackground,
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(
                        color: isDone ? AppColors.meadowGreen.withOpacity(0.4) : AppColors.borderColor,
                      ),
                    ),
                    padding: const EdgeInsets.all(12),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(
                              isDone ? Icons.check_circle_rounded : Icons.menu_book_rounded,
                              color: isDone ? AppColors.meadowGreen : AppColors.primaryBlue,
                              size: 22,
                            ),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                topic.localizedTitle(lang),
                                style: TextStyle(
                                  fontSize: 15,
                                  fontWeight: FontWeight.bold,
                                  color: isDone ? AppColors.darkGreen : AppColors.textDark,
                                ),
                              ),
                            ),
                            InkWell(
                              borderRadius: BorderRadius.circular(8),
                              onTap: () => onTopicTap(topic),
                              child: Container(
                                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                decoration: BoxDecoration(
                                  color: AppColors.lightBlue,
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Text(
                                  lang == 'te' ? 'చదువు ➔' : 'Study ➔',
                                  style: const TextStyle(
                                    fontSize: 12,
                                    fontWeight: FontWeight.bold,
                                    color: AppColors.primaryBlue,
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 6),
                        // Topic Concept Information
                        Text(
                          topic.localizedExplanation(lang),
                          style: const TextStyle(
                            fontSize: 13,
                            height: 1.4,
                            color: AppColors.textDark,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          lang == 'te'
                              ? '⏱️ ${topic.durationMinutes} నిమిషాలు • ${topic.practiceQuestionCount} అభ్యాస ప్రశ్నలు'
                              : '⏱️ ${topic.durationMinutes} mins • ${topic.practiceQuestionCount} practice questions',
                          style: const TextStyle(fontSize: 11, color: AppColors.textMuted),
                        ),
                      ],
                    ),
                  );
                },
              ),
              const SizedBox(height: 14),

              // Chapter video: shown after ALL topics of this chapter
              ChapterVideoSection(chapter: chapter),
            ],
          ),
        ),
      ),
    );
  }
}

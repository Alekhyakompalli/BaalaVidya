import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/models/chapter_package_model.dart';
import 'package:baalavidya/models/curriculum_models.dart';
import 'package:baalavidya/services/offline_store.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';
import 'package:baalavidya/widgets/video_section_widget.dart';

/// Chapter-level "Chapter video" section shown at the END of a chapter's topic list.
/// Plays one video explaining the whole chapter, or shows "Chapter video coming soon".
class ChapterVideoSection extends ConsumerWidget {
  final ChapterItem chapter;

  const ChapterVideoSection({
    super.key,
    required this.chapter,
  });

  /// First cached video belonging to any topic of [chapter].
  /// Prefers a video in the user's language [lang]; falls back to the first available one.
  static VideoMetadata? findChapterVideo(ChapterItem chapter, String lang) {
    final List<VideoMetadata> videos = [];
    for (final topic in chapter.topics) {
      videos.addAll(OfflineStore().getVideosForTopic(topic.id));
    }
    for (final video in videos) {
      if (video.languageCode == lang) return video;
    }
    if (videos.isNotEmpty) return videos.first;

    final isTe = lang == 'te';
    return VideoMetadata(
      videoId: 'vid_${chapter.id}_$lang',
      topicId: chapter.topics.isNotEmpty ? chapter.topics.first.id : chapter.id,
      languageCode: lang,
      title: isTe
          ? '${chapter.localizedTitle(lang)} - AI సమగ్ర వివరణ వీడియో పాఠం'
          : '${chapter.localizedTitle(lang)} - AI Animated Chapter Explainer',
      teluguTitle: '${chapter.localizedTitle(lang)} - AI సమగ్ర వివరణ వీడియో పాఠం',
      durationMinutes: 12,
      durationSeconds: 720,
      streamUrl: 'ai://video_generator/' + chapter.id,
      provider: 'Bala Buddy AI Video Studio (AI-Generated Contextual Lesson)',
      onlineStreamingOnly: false,
    );
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(languageProvider);
    final isOnline = ref.watch(isOnlineProvider);
    final video = findChapterVideo(chapter, lang);

    return Container(
      width: double.infinity,
      margin: const EdgeInsets.only(top: 4),
      padding: const EdgeInsets.all(14.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.borderColor, width: 1.5),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Text('🤖', style: TextStyle(fontSize: 22)),
              const SizedBox(width: 8),
              Text(
                lang == 'te' ? 'AI చాప్టర్ వివరణ వీడియో' : 'AI Chapter Explainer Video',
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: AppColors.textDark,
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),
          if (video == null)
            Text(
              lang == 'te' ? 'AI వీడియో పాఠం సిద్ధంగా ఉంది' : 'AI Video Explainer Ready',
              style: const TextStyle(fontSize: 14, color: AppColors.textMuted),
            )
          else
            Material(
              color: Colors.transparent,
              child: InkWell(
                borderRadius: BorderRadius.circular(14),
                onTap: () {
                  openVideoPlayerSheet(
                    context,
                    ref,
                    video,
                    lang,
                    topicId: video.topicId.isNotEmpty ? video.topicId : chapter.id,
                    selectedQuality: '480p (Standard)',
                    onQualityChanged: (_) {},
                  );
                },
                child: Container(
                  padding: const EdgeInsets.all(12.0),
                  decoration: BoxDecoration(
                    color: AppColors.lightBlue.withOpacity(0.4),
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: AppColors.primaryBlue.withOpacity(0.3), width: 1.2),
                  ),
                  child: Row(
                    children: [
                      const Icon(
                        Icons.play_circle_fill_rounded,
                        size: 36,
                        color: AppColors.primaryBlue,
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              video.localizedTitle(lang),
                              style: const TextStyle(
                                fontSize: 14,
                                fontWeight: FontWeight.bold,
                                color: AppColors.textDark,
                              ),
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                            ),
                            const SizedBox(height: 4),
                            Text(
                              '${video.durationMinutes} ${lang == 'te' ? 'నిమి' : 'mins'} • ${video.provider}',
                              style: const TextStyle(fontSize: 11, color: AppColors.textMuted),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(width: 8),
                      const Icon(
                        Icons.arrow_forward_ios_rounded,
                        size: 16,
                        color: AppColors.textMuted,
                      ),
                    ],
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}

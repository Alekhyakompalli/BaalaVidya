import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/models/curriculum_models.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';

/// Subject card for Class Selection screen.
/// Displays subject icon, title in selected language, chapter count, and progress bar.
class SubjectCard extends ConsumerWidget {
  final SubjectItem subject;
  final VoidCallback onTap;

  const SubjectCard({
    super.key,
    required this.subject,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(languageProvider);

    return Container(
      constraints: const BoxConstraints(minHeight: 110),
      margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 4),
      child: Card(
        color: Colors.white,
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
          side: BorderSide(
            color: subject.isAvailable ? subject.color.withOpacity(0.3) : AppColors.borderColor,
            width: 1.5,
          ),
        ),
        child: InkWell(
          borderRadius: BorderRadius.circular(20),
          onTap: subject.isAvailable ? onTap : null,
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              children: [
                // Leading emoji badge
                Container(
                  width: 60,
                  height: 60,
                  decoration: BoxDecoration(
                    color: subject.lightColor,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  alignment: Alignment.center,
                  child: Text(
                    subject.iconEmoji,
                    style: const TextStyle(fontSize: 32),
                  ),
                ),
                const SizedBox(width: 16),
                // Subject info
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Row(
                        children: [
                          Expanded(
                            child: Text(
                              subject.localizedName(lang),
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: subject.isAvailable ? AppColors.textDark : AppColors.textMuted,
                              ),
                            ),
                          ),
                          if (!subject.isAvailable)
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                              decoration: BoxDecoration(
                                color: AppColors.lightOrange,
                                borderRadius: BorderRadius.circular(10),
                              ),
                              child: Text(
                                lang == 'te' ? 'త్వరలో' : 'Coming Soon',
                                style: const TextStyle(
                                  fontSize: 12,
                                  fontWeight: FontWeight.bold,
                                  color: AppColors.coralOrange,
                                ),
                              ),
                            ),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Text(
                        subject.localizedOverview(lang),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                        style: const TextStyle(
                          fontSize: 14,
                          color: AppColors.textMuted,
                        ),
                      ),
                      if (subject.isAvailable) ...[
                        const SizedBox(height: 8),
                        Row(
                          children: [
                            Text(
                              lang == 'te'
                                  ? '${subject.chapterCount} పాఠాలు'
                                  : '${subject.chapterCount} Lessons',
                              style: TextStyle(
                                fontSize: 13,
                                fontWeight: FontWeight.w600,
                                color: subject.color,
                              ),
                            ),
                            const Spacer(),
                            Text(
                              '${subject.progressPercentage}%',
                              style: TextStyle(
                                fontSize: 13,
                                fontWeight: FontWeight.bold,
                                color: subject.color,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 4),
                        ClipRRect(
                          borderRadius: BorderRadius.circular(6),
                          child: LinearProgressIndicator(
                            value: subject.progressPercentage / 100.0,
                            minHeight: 6,
                            backgroundColor: AppColors.borderColor,
                            valueColor: AlwaysStoppedAnimation<Color>(subject.color),
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
                if (subject.isAvailable) ...[
                  const SizedBox(width: 8),
                  Icon(
                    Icons.chevron_right_rounded,
                    color: subject.color,
                    size: 32,
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}

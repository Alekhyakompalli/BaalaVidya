import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';

/// The 4 Next Steps interactive action bar required by [PS: Interactive Learning; docs/eval.md:113]:
/// 1. Play Game (ఆట ఆడండి)
/// 2. Practice Workbook (వర్క్‌బుక్ చేయండి)
/// 3. Watch Video (వీడియో చూడండి)
/// 4. Ask Doubts (సందేహాలు అడగండి)
class NextStepsBar extends ConsumerWidget {
  final VoidCallback onPlayGame;
  final VoidCallback onPracticeWorkbook;
  final VoidCallback onWatchVideo;
  final VoidCallback onAskDoubts;

  const NextStepsBar({
    super.key,
    required this.onPlayGame,
    required this.onPracticeWorkbook,
    required this.onWatchVideo,
    required this.onAskDoubts,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(languageProvider);

    return Container(
      padding: const EdgeInsets.all(16.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppColors.borderColor, width: 1.5),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 8,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Text('🎯', style: TextStyle(fontSize: 22)),
              const SizedBox(width: 8),
              Text(
                lang == 'te' ? 'తదుపరి అభ్యాసాలు (Next Steps):' : 'What would you like to do next?',
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: AppColors.textDark,
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),
          // 4 Action Buttons Grid / Row
          Wrap(
            spacing: 10,
            runSpacing: 10,
            children: [
              _buildStepButton(
                context: context,
                emoji: '🎮',
                title: lang == 'te' ? 'ఆట ఆడండి' : 'Play Game',
                subtitle: lang == 'te' ? 'క్విజ్ గేమ్' : 'Concept Game',
                color: AppColors.candyPurple,
                lightColor: AppColors.lightPurple,
                onTap: onPlayGame,
              ),
              _buildStepButton(
                context: context,
                emoji: '📝',
                title: lang == 'te' ? 'వర్క్‌బుక్ చేయండి' : 'Practice Workbook',
                subtitle: lang == 'te' ? 'అభ్యాసాలు' : 'Questions',
                color: AppColors.coralOrange,
                lightColor: AppColors.lightOrange,
                onTap: onPracticeWorkbook,
              ),
              _buildStepButton(
                context: context,
                emoji: '📖',
                title: lang == 'te' ? 'పాఠ్యపుస్తకం' : 'Textbook PDF',
                subtitle: lang == 'te' ? 'SCERT భాగం' : 'PDF Passage',
                color: AppColors.primaryBlue,
                lightColor: AppColors.lightBlue,
                onTap: onWatchVideo,
              ),
              _buildStepButton(
                context: context,
                emoji: '💬',
                title: lang == 'te' ? 'సందేహాలు అడగండి' : 'Ask Doubts',
                subtitle: lang == 'te' ? 'బాల బడ్డీ' : 'Bala Buddy',
                color: AppColors.meadowGreen,
                lightColor: AppColors.lightGreen,
                onTap: onAskDoubts,
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildStepButton({
    required BuildContext context,
    required String emoji,
    required String title,
    required String subtitle,
    required Color color,
    required Color lightColor,
    required VoidCallback onTap,
  }) {
    return Container(
      constraints: const BoxConstraints(minHeight: 52, minWidth: 140),
      child: Material(
        color: lightColor,
        borderRadius: BorderRadius.circular(16),
        child: InkWell(
          borderRadius: BorderRadius.circular(16),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(emoji, style: const TextStyle(fontSize: 24)),
                const SizedBox(width: 8),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      title,
                      style: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.bold,
                        color: color,
                      ),
                    ),
                    Text(
                      subtitle,
                      style: const TextStyle(
                        fontSize: 12,
                        color: AppColors.textMuted,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

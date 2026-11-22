import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/l10n/app_strings.dart';
import 'package:baalavidya/models/chapter_package_model.dart';
import 'package:baalavidya/services/offline_store.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';
import 'package:baalavidya/widgets/certificate_widget.dart';
import 'package:baalavidya/widgets/language_toggle.dart';
import 'package:baalavidya/widgets/offline_banner.dart';

/// Full Learning Progress & Gamification Screen [PS: 9. Learning Progress; 11. Play & Learn Module].
/// Displays:
/// - Total XP, Current Level, Level Title, Progress to next level
/// - Learning Streak with day definition (consecutive calendar days in IST)
/// - Coins (Learning Points) & Stars
/// - Completed Topics, Chapters Covered, Questions Asked
/// - Topic Mastery status per topic (Beginner, Learning, Practicing, Mastered)
/// - Badges collection
/// - Progress-based Unlockables
/// - Certificates gallery
class LearningProgressScreen extends ConsumerWidget {
  const LearningProgressScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(languageProvider);
    final xp = ref.watch(learnerXpProvider);
    final level = ref.watch(learnerLevelProvider);
    final levelName = ref.watch(learnerLevelNameProvider);
    final streak = ref.watch(learnerStreakProvider);
    final coins = ref.watch(learnerCoinsProvider);
    final stars = ref.watch(learnerStarsProvider);
    final questionsAsked = ref.watch(questionsAskedProvider);
    final completedTopics = ref.watch(completedTopicsProvider);
    final badges = ref.watch(learnerBadgesProvider);
    final masteryScores = ref.watch(topicMasteryScoresProvider);
    final certificates = ref.watch(certificatesProvider);

    // Calculate XP progress to next level
    final xpInCurrentLevel = xp % 100;
    final xpToNext = 100 - xpInCurrentLevel;

    return Scaffold(
      backgroundColor: AppColors.softBackground,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        title: Text(
          AppStrings.get('progressScreenTitle', lang),
          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppColors.textDark),
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
                    // 1. Level & XP Hero Banner
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(20.0),
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          colors: [AppColors.primaryBlue, AppColors.darkBlue],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                        borderRadius: BorderRadius.circular(24),
                        boxShadow: [
                          BoxShadow(
                            color: AppColors.primaryBlue.withOpacity(0.3),
                            blurRadius: 10,
                            offset: const Offset(0, 4),
                          ),
                        ],
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Container(
                                padding: const EdgeInsets.all(10),
                                decoration: const BoxDecoration(
                                  color: Colors.white24,
                                  shape: BoxShape.circle,
                                ),
                                child: const Text('🏆', style: TextStyle(fontSize: 32)),
                              ),
                              const SizedBox(width: 14),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      '${AppStrings.get('currentLevel', lang)} $level',
                                      style: const TextStyle(
                                        fontSize: 20,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.white,
                                      ),
                                    ),
                                    const SizedBox(height: 2),
                                    Text(
                                      levelName,
                                      style: const TextStyle(
                                        fontSize: 14,
                                        fontWeight: FontWeight.w600,
                                        color: AppColors.sunshineYellow,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                decoration: BoxDecoration(
                                  color: AppColors.sunshineYellow,
                                  borderRadius: BorderRadius.circular(16),
                                ),
                                child: Text(
                                  '$xp XP ⚡',
                                  style: const TextStyle(
                                    fontSize: 15,
                                    fontWeight: FontWeight.bold,
                                    color: AppColors.textDark,
                                  ),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 18),
                          // XP Progress to next level
                          ClipRRect(
                            borderRadius: BorderRadius.circular(8),
                            child: LinearProgressIndicator(
                              value: xpInCurrentLevel / 100.0,
                              minHeight: 10,
                              backgroundColor: Colors.white24,
                              valueColor: const AlwaysStoppedAnimation<Color>(AppColors.sunshineYellow),
                            ),
                          ),
                          const SizedBox(height: 6),
                          Text(
                            lang == 'te'
                                ? 'తదుపరి స్థాయికి ఇంకా $xpToNext XP కావాలి'
                                : '$xpToNext XP to Level ${level + 1}',
                            style: const TextStyle(fontSize: 12, color: Colors.white70),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),

                    // 2. Metrics Quick Grid: Streak, Coins, Stars, Questions
                    Row(
                      children: [
                        _buildMetricCard(
                          emoji: '🔥',
                          title: AppStrings.get('learningStreak', lang),
                          value: '$streak ${AppStrings.get('daysCount', lang)}',
                          subtitle: AppStrings.get('streakDefinition', lang),
                          color: AppColors.coralOrange,
                          lightColor: AppColors.lightOrange,
                        ),
                        const SizedBox(width: 12),
                        _buildMetricCard(
                          emoji: '🪙',
                          title: AppStrings.get('coinsLabel', lang),
                          value: '$coins',
                          subtitle: '1 Coin = 1 Point',
                          color: Colors.amber.shade800,
                          lightColor: Colors.amber.shade100,
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        _buildMetricCard(
                          emoji: '⭐',
                          title: AppStrings.get('starsLabel', lang),
                          value: '$stars ⭐',
                          subtitle: 'Workbook mastery',
                          color: Colors.amber.shade900,
                          lightColor: AppColors.lightYellow,
                        ),
                        const SizedBox(width: 12),
                        _buildMetricCard(
                          emoji: '💬',
                          title: AppStrings.get('questionsAsked', lang),
                          value: '$questionsAsked',
                          subtitle: 'Bala Buddy doubts',
                          color: AppColors.meadowGreen,
                          lightColor: AppColors.lightGreen,
                        ),
                      ],
                    ),
                    const SizedBox(height: 20),

                    // 3. Topic Mastery Breakdown [PS: 11. Topic Mastery Score]
                    Row(
                      children: [
                        const Text('🌱', style: TextStyle(fontSize: 22)),
                        const SizedBox(width: 8),
                        Text(
                          AppStrings.get('topicMastery', lang),
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: AppColors.textDark,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    ...masteryScores.entries.map((entry) {
                      final scoreModel = entry.value;
                      return Container(
                        margin: const EdgeInsets.only(bottom: 10),
                        padding: const EdgeInsets.all(14),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(color: AppColors.borderColor),
                        ),
                        child: Row(
                          children: [
                            Text(scoreModel.badgeEmoji, style: const TextStyle(fontSize: 28)),
                            const SizedBox(width: 12),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    entry.key == 'bio_ch1_t1'
                                        ? (lang == 'te' ? 'కిరణజన్య సంయోగక్రియ' : 'What is Photosynthesis?')
                                        : (lang == 'te' ? 'కాంతి మరియు నిష్కాంతి చర్యలు' : 'Light & Dark Reactions'),
                                    style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                                  ),
                                  const SizedBox(height: 2),
                                  Text(
                                    scoreModel.localizedLevel(lang),
                                    style: const TextStyle(fontSize: 13, color: AppColors.textMuted),
                                  ),
                                ],
                              ),
                            ),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                              decoration: BoxDecoration(
                                color: AppColors.lightGreen,
                                borderRadius: BorderRadius.circular(10),
                              ),
                              child: Text(
                                '${scoreModel.totalScore}%',
                                style: const TextStyle(fontWeight: FontWeight.bold, color: AppColors.darkGreen),
                              ),
                            ),
                          ],
                        ),
                      );
                    }),
                    const SizedBox(height: 18),

                    // 4. Badges Collection [PS: 11. Learning Rewards]
                    Row(
                      children: [
                        const Text('🏅', style: TextStyle(fontSize: 22)),
                        const SizedBox(width: 8),
                        Text(
                          AppStrings.get('badgesShowcase', lang),
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: AppColors.textDark,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Wrap(
                      spacing: 12,
                      runSpacing: 12,
                      children: [
                        _buildBadgeChip(
                          id: 'explorer',
                          title: lang == 'te' ? 'అన్వేషకుడు 🧭' : 'Explorer 🧭',
                          subtitle: 'First topic read',
                          isUnlocked: badges.contains('explorer'),
                        ),
                        _buildBadgeChip(
                          id: 'science_genius',
                          title: lang == 'te' ? 'సైన్స్ జీనియస్ 🔬' : 'Science Genius 🔬',
                          subtitle: 'Science workbook done',
                          isUnlocked: badges.contains('science_genius'),
                        ),
                        _buildBadgeChip(
                          id: 'mission_master',
                          title: lang == 'te' ? 'మిషన్ మాస్టర్ 🏅' : 'Mission Master 🏅',
                          subtitle: 'Chapter 1 challenge',
                          isUnlocked: badges.contains('mission_master'),
                        ),
                        _buildBadgeChip(
                          id: 'streak_star',
                          title: lang == 'te' ? 'స్ట్రీక్ స్టార్ 🔥' : 'Streak Star 🔥',
                          subtitle: '5-day learning streak',
                          isUnlocked: streak >= 5,
                        ),
                      ],
                    ),
                    const SizedBox(height: 20),

                    // 5. Achievement Certificates Gallery [PS: 11. Learning Rewards]
                    Row(
                      children: [
                        const Text('📜', style: TextStyle(fontSize: 22)),
                        const SizedBox(width: 8),
                        Text(
                          AppStrings.get('certificatesGallery', lang),
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: AppColors.textDark,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    if (certificates.isEmpty)
                      const Text('Complete chapter mission challenges to earn certificates!')
                    else
                      ...certificates.map((cert) => CertificateWidget(certificate: cert)),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMetricCard({
    required String emoji,
    required String title,
    required String value,
    required String subtitle,
    required Color color,
    required Color lightColor,
  }) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(18),
          border: Border.all(color: color.withOpacity(0.3), width: 1.5),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text(emoji, style: const TextStyle(fontSize: 24)),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    title,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppColors.textMuted),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(value, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: color)),
            const SizedBox(height: 2),
            Text(
              subtitle,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(fontSize: 10, color: AppColors.textMuted),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildBadgeChip({
    required String id,
    required String title,
    required String subtitle,
    required bool isUnlocked,
  }) {
    return Container(
      width: 160,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: isUnlocked ? Colors.white : AppColors.softBackground,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isUnlocked ? AppColors.sunshineYellow : AppColors.borderColor,
          width: 1.5,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  title,
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: isUnlocked ? AppColors.textDark : AppColors.textMuted,
                  ),
                ),
              ),
              if (!isUnlocked)
                const Icon(Icons.lock_rounded, size: 16, color: AppColors.textMuted),
            ],
          ),
          const SizedBox(height: 4),
          Text(
            subtitle,
            style: const TextStyle(fontSize: 11, color: AppColors.textMuted),
          ),
        ],
      ),
    );
  }
}

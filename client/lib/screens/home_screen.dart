import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/models/curriculum_models.dart';
import 'package:baalavidya/models/mock_data.dart';
import 'package:baalavidya/screens/chatbot_screen.dart';
import 'package:baalavidya/screens/class_selection_screen.dart';
import 'package:baalavidya/screens/learning_progress_screen.dart';
import 'package:baalavidya/screens/parent_dashboard_screen.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';
import 'package:baalavidya/widgets/class_card.dart';
import 'package:baalavidya/widgets/language_toggle.dart';
import 'package:baalavidya/widgets/learner_switcher.dart';
import 'package:baalavidya/widgets/offline_banner.dart';

/// Home Screen adhering to [PS: 2. Home Screen; Supported Languages].
/// Features:
/// - Friendly Bala Buddy greeting and learner XP counter.
/// - Language toggle at the top right (EN <-> తెలుగు).
/// - Search bar for topics and concepts.
/// - Class Selection Grid for Class 1 to Class 10.
/// - Tapping any class navigates to ClassSelectionScreen (Tap 1).
class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(languageProvider);
    final xp = ref.watch(learnerXpProvider);
    final learnerName = ref.watch(currentLearnerNameProvider);
    final selectedClass = ref.watch(selectedClassProvider);

    return Scaffold(
      backgroundColor: AppColors.softBackground,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        titleSpacing: 16,
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: AppColors.lightYellow,
                shape: BoxShape.circle,
                border: Border.all(color: AppColors.sunshineYellow, width: 2),
              ),
              child: const Text('🤖', style: TextStyle(fontSize: 22)),
            ),
            const SizedBox(width: 10),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  lang == 'te' ? 'నమస్తే $learnerName! 🌟' : 'Hello, $learnerName! 🌟',
                  style: const TextStyle(
                    fontSize: 17,
                    fontWeight: FontWeight.bold,
                    color: AppColors.textDark,
                  ),
                ),
                Text(
                  lang == 'te'
                      ? '${selectedClass.localizedName(lang)} • బాల బడ్డీతో నేర్చుకుందాం'
                      : '${selectedClass.localizedName(lang)} • Ready to explore?',
                  style: const TextStyle(fontSize: 12, color: AppColors.textMuted),
                ),
              ],
            ),
          ],
        ),
        actions: const [
          ConnectionStatusBadge(),
          LearnerSwitcher(),
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
              // Search Bar
              Container(
                height: 52,
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AppColors.borderColor, width: 1.5),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.04),
                      blurRadius: 6,
                      offset: const Offset(0, 2),
                    ),
                  ],
                ),
                child: TextField(
                  onChanged: (val) {
                    ref.read(searchQueryProvider.notifier).state = val;
                  },
                  decoration: InputDecoration(
                    hintText: lang == 'te'
                        ? 'పాఠాలు లేదా భావనలను వెతకండి...'
                        : 'Search topics, lessons, concepts...',
                    hintStyle: const TextStyle(color: AppColors.textMuted, fontSize: 16),
                    prefixIcon: const Icon(Icons.search_rounded, color: AppColors.primaryBlue),
                    suffixIcon: const Icon(Icons.mic_rounded, color: AppColors.coralOrange),
                    border: InputBorder.none,
                    contentPadding: const EdgeInsets.symmetric(vertical: 14),
                  ),
                ),
              ),
              const SizedBox(height: 16),

              // Gamification XP & Streak Banner (Tappable -> LearningProgressScreen)
              Material(
                color: Colors.transparent,
                child: InkWell(
                  borderRadius: BorderRadius.circular(20),
                  onTap: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(builder: (context) => const LearningProgressScreen()),
                    );
                  },
                  child: Container(
                    padding: const EdgeInsets.all(14.0),
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(
                        colors: [AppColors.primaryBlue, AppColors.darkBlue],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      borderRadius: BorderRadius.circular(20),
                      boxShadow: [
                        BoxShadow(
                          color: AppColors.primaryBlue.withOpacity(0.3),
                          blurRadius: 8,
                          offset: const Offset(0, 4),
                        ),
                      ],
                    ),
                    child: Row(
                      children: [
                        const Text('🏆', style: TextStyle(fontSize: 32)),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                lang == 'te' ? 'అభ్యాస పురోగతి & బహుమతులు 🌟' : 'Learning Progress & Rewards 🌟',
                                style: const TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.white,
                                ),
                              ),
                              const SizedBox(height: 2),
                              Text(
                                lang == 'te'
                                    ? 'స్థాయి, బ్యాడ్జీలు & సర్టిఫికేట్లు చూడటానికి ట్యాప్ చేయండి'
                                    : 'Tap to view level, badges & certificates ➔',
                                style: const TextStyle(
                                  fontSize: 12,
                                  color: AppColors.lightBlue,
                                ),
                              ),
                            ],
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                          decoration: BoxDecoration(
                            color: AppColors.sunshineYellow,
                            borderRadius: BorderRadius.circular(14),
                          ),
                          child: Text(
                            '$xp XP ⚡',
                            style: const TextStyle(
                              fontSize: 14,
                              fontWeight: FontWeight.bold,
                              color: AppColors.textDark,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 12),

              // Parent Zone Quick Entry [PS: 10. Parent Dashboard; R11]
              Material(
                color: Colors.transparent,
                child: InkWell(
                  borderRadius: BorderRadius.circular(16),
                  onTap: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(builder: (context) => const ParentDashboardScreen()),
                    );
                  },
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 14.0, vertical: 10.0),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: const Color(0xFFD5D8DC)),
                    ),
                    child: Row(
                      children: [
                        const Text('👨‍👩‍👧', style: TextStyle(fontSize: 24)),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                AppStrings.get('parentZoneTitle', lang),
                                style: const TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold,
                                  color: AppColors.textDark,
                                ),
                              ),
                              Text(
                                lang == 'te'
                                    ? 'సమయం, నైపుణ్యాలు & తల్లిదండ్రుల సూచనలు ➔'
                                    : 'View learning time, weak areas & tips ➔',
                                style: const TextStyle(fontSize: 11, color: AppColors.textMuted),
                              ),
                            ],
                          ),
                        ),
                        const Icon(Icons.lock_outline, size: 18, color: AppColors.textMuted),
                      ],
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 22),

              // Class Selection Section Header
              Row(
                children: [
                  const Text('🎒', style: TextStyle(fontSize: 22)),
                  const SizedBox(width: 8),
                  Text(
                    lang == 'te' ? 'మీ తరగతిని ఎంచుకోండి:' : 'Select Your Class:',
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: AppColors.textDark,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),

              // Class 1 to Class 10 Grid (Navigation Tap 1)
              GridView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  crossAxisSpacing: 12,
                  mainAxisSpacing: 12,
                  childAspectRatio: 1.15,
                ),
                itemCount: MockCurriculumData.classes.length,
                itemBuilder: (context, index) {
                  final classItem = MockCurriculumData.classes[index];
                  return ClassCard(
                    classItem: classItem,
                    onTap: () {
                      ref.read(selectedClassProvider.notifier).state = classItem;
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (context) => ClassSelectionScreen(classItem: classItem),
                        ),
                      );
                    },
                  );
                },
              ),
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
          lang == 'te' ? 'బాల బడ్డీ చాట్' : 'Ask Bala Buddy',
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
        ),
        onPressed: () {
          Navigator.of(context).push(
            MaterialPageRoute(builder: (context) => const ChatbotScreen()),
          );
        },
      ),
    );
  }
}

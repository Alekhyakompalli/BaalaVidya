import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/models/chapter_package_model.dart';
import 'package:baalavidya/services/offline_store.dart';
import 'package:baalavidya/services/sync_queue_service.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';
import 'package:baalavidya/widgets/language_toggle.dart';
import 'package:baalavidya/widgets/offline_banner.dart';

/// Story Mode Screen for Classes 1 to 5 [PS: 11. Story-Based Learning].
/// Converts foundational concepts into playful cartoon stories and interactive narrative choices.
class StoryModeScreen extends ConsumerStatefulWidget {
  const StoryModeScreen({super.key});

  @override
  ConsumerState<StoryModeScreen> createState() => _StoryModeScreenState();
}

class _StoryModeScreenState extends ConsumerState<StoryModeScreen> {
  int _currentStepIndex = 0;
  int? _selectedChoice;
  bool _revealed = false;

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);
    final pkg = OfflineStore().getChapterPackage('bio_ch1');
    final steps = pkg?.storySteps ?? [];

    if (steps.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: const Text('Story Adventures')),
        body: const Center(child: Text('No story adventures available.')),
      );
    }

    final step = steps[_currentStepIndex];
    final choices = step.localizedChoices(lang);

    return Scaffold(
      backgroundColor: const Color(0xFFF9FBF7),
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        title: Text(
          lang == 'te' ? 'కథల రూపంలో చదువు 🐰' : 'Story Adventure: Bala Rabbit 🐰',
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
                  children: [
                    // Cartoon Character & Narrative Card
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(20.0),
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          colors: [Color(0xFFE8F5E9), Color(0xFFC8E6C9)],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                        borderRadius: BorderRadius.circular(24),
                        border: Border.all(color: AppColors.meadowGreen, width: 2),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.04),
                            blurRadius: 8,
                            offset: const Offset(0, 3),
                          ),
                        ],
                      ),
                      child: Column(
                        children: [
                          // Animated character avatar
                          Container(
                            width: 84,
                            height: 84,
                            decoration: const BoxDecoration(
                              color: Colors.white,
                              shape: BoxShape.circle,
                            ),
                            alignment: Alignment.center,
                            child: Text(step.characterEmoji, style: const TextStyle(fontSize: 48)),
                          ),
                          const SizedBox(height: 14),
                          Text(
                            lang == 'te'
                                ? 'బాల కుందేలు సాహసం (అధ్యాయం ${_currentStepIndex + 1})'
                                : 'Bala Rabbit Adventure (Episode ${_currentStepIndex + 1})',
                            style: const TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                              color: AppColors.darkGreen,
                            ),
                          ),
                          const SizedBox(height: 12),
                          Text(
                            step.localizedNarrative(lang),
                            textAlign: TextAlign.center,
                            style: const TextStyle(fontSize: 16, height: 1.5, color: AppColors.textDark),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 20),

                    // Interactive Decision Prompt Card
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(18.0),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: AppColors.borderColor, width: 1.5),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              const Text('🎯', style: TextStyle(fontSize: 22)),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  step.localizedQuestionPrompt(lang),
                                  style: const TextStyle(
                                    fontSize: 17,
                                    fontWeight: FontWeight.bold,
                                    color: AppColors.textDark,
                                  ),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 16),

                          // Choice Options
                          ...List.generate(choices.length, (idx) {
                            final isSelected = _selectedChoice == idx;
                            Color borderCol = AppColors.borderColor;
                            Color bgCol = Colors.white;

                            if (_revealed) {
                              if (idx == step.correctChoiceIndex) {
                                borderCol = AppColors.meadowGreen;
                                bgCol = AppColors.lightGreen;
                              } else if (isSelected) {
                                borderCol = Colors.red;
                                bgCol = const Color(0xFFFFEBEE);
                              }
                            } else if (isSelected) {
                              borderCol = AppColors.coralOrange;
                              bgCol = AppColors.lightOrange;
                            }

                            return Container(
                              margin: const EdgeInsets.only(bottom: 10),
                              constraints: const BoxConstraints(minHeight: 52),
                              child: Material(
                                color: bgCol,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(14),
                                  side: BorderSide(color: borderCol, width: 2),
                                ),
                                child: InkWell(
                                  borderRadius: BorderRadius.circular(14),
                                  onTap: _revealed ? null : () => setState(() => _selectedChoice = idx),
                                  child: Padding(
                                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                                    child: Row(
                                      children: [
                                        Text(String.fromCharCode(65 + idx),
                                            style: const TextStyle(fontWeight: FontWeight.bold)),
                                        const SizedBox(width: 14),
                                        Expanded(
                                          child: Text(
                                            choices[idx],
                                            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                                          ),
                                        ),
                                        if (_revealed && idx == step.correctChoiceIndex)
                                          const Icon(Icons.check_circle_rounded, color: AppColors.meadowGreen),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                            );
                          }),

                          if (_revealed) ...[
                            const SizedBox(height: 12),
                            Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: AppColors.lightYellow,
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Row(
                                children: [
                                  const Text('🌟', style: TextStyle(fontSize: 22)),
                                  const SizedBox(width: 10),
                                  Expanded(
                                    child: Text(
                                      step.localizedTakeaway(lang),
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
                            const SizedBox(height: 16),
                            ElevatedButton(
                              style: ElevatedButton.styleFrom(
                                backgroundColor: AppColors.primaryBlue,
                                foregroundColor: Colors.white,
                                minimumSize: const Size(double.infinity, 50),
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                              ),
                              onPressed: () {
                                if (_currentStepIndex + 1 < steps.length) {
                                  setState(() {
                                    _currentStepIndex++;
                                    _selectedChoice = null;
                                    _revealed = false;
                                  });
                                } else {
                                  Navigator.of(context).pop();
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    SnackBar(
                                      content: Text(
                                        lang == 'te'
                                            ? 'కథా ప్రయాణం పూర్తయింది! 30 XP సంపాదించారు! 🥕'
                                            : 'Story Adventure Complete! You earned 30 XP! 🥕',
                                      ),
                                    ),
                                  );
                                }
                              },
                              child: Text(
                                _currentStepIndex + 1 < steps.length ? 'Next Episode 🥕' : 'Finish Adventure 🌟',
                                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                              ),
                            ),
                          ] else ...[
                            const SizedBox(height: 12),
                            ElevatedButton(
                              style: ElevatedButton.styleFrom(
                                backgroundColor: AppColors.coralOrange,
                                foregroundColor: Colors.white,
                                minimumSize: const Size(double.infinity, 50),
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                              ),
                              onPressed: _selectedChoice == null
                                  ? null
                                  : () {
                                      setState(() {
                                        _revealed = true;
                                        ref.read(learnerXpProvider.notifier).state += 15;
                                        ref.read(learnerCoinsProvider.notifier).state += 5;
                                        SyncQueueService().enqueueEvent(
                                          learnerId: ref.read(currentLearnerIdProvider),
                                          eventType: 'story_step_completed',
                                          payload: {'episode': _currentStepIndex, 'character': 'bala_rabbit'},
                                        );
                                      });
                                    },
                              child: const Text('Confirm Answer 🥕',
                                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                            ),
                          ],
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

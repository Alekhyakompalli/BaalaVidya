import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/l10n/app_strings.dart';
import 'package:baalavidya/services/sync_queue_service.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';
import 'package:baalavidya/widgets/language_toggle.dart';
import 'package:baalavidya/widgets/offline_banner.dart';

/// AI Generated Personalized Practice Screen [PS: 11. AI Generated Personalized Practice].
/// Generates simplified analogies and booster exercises when a student struggles with a topic.
class PersonalizedPracticeScreen extends ConsumerStatefulWidget {
  final String topicId;
  final String topicTitle;

  const PersonalizedPracticeScreen({
    super.key,
    required this.topicId,
    required this.topicTitle,
  });

  @override
  ConsumerState<PersonalizedPracticeScreen> createState() => _PersonalizedPracticeScreenState();
}

class _PersonalizedPracticeScreenState extends ConsumerState<PersonalizedPracticeScreen> {
  int _currentStep = 0;
  int? _selectedOption;
  bool _submitted = false;
  int _bonusXpEarned = 0;

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);

    final isBiology = widget.topicId.contains('bio') || widget.topicTitle.toLowerCase().contains('photo');

    final simplifiedExplanationEn = isBiology
        ? 'Think of plants as little green chefs! 🌿 Instead of a gas stove, they use gentle sunlight. '
            'Instead of tap water, they sip fresh water from roots. With a pinch of clean air, they bake delicious glucose treats and gift us pure oxygen to breathe!'
        : 'Think of fractions like sharing a yummy pizza with your best friends! 🍕 '
            'If you slice 1 pizza into 2 equal halves, each friend gets 1/2. If you share among 4 friends, each gets 1/4!';

    final simplifiedExplanationTe = isBiology
        ? 'మొక్కలను మన తోటలోని చిన్న ఆకుపచ్చ చెఫ్‌లుగా ఊహించుకోండి! 🌿 అవి సూర్యరశ్మి అనే శక్తితో, '
            'వేర్ల ద్వారా నీటిని, గాలి ద్వారా కార్బన్ డయాక్సైడ్ తీసుకొని తియ్యని గ్లూకోజ్ ఆహారాన్ని తయారుచేస్తాయి. మనకు స్వచ్ఛమైన ఆక్సిజన్ గాలిని అందిస్తాయి!'
        : 'భిన్నాలను మీ స్నేహితులతో రుచికరమైన పిజ్జాను పంచుకోవడంగా ఊహించుకోండి! 🍕 '
            'ఒక పిజ్జాను 2 సమాన భాగాలు చేస్తే, ఒక్కొక్కరికి 1/2 భాగం వస్తుంది. 4 భాగాలు చేస్తే 1/4 వస్తుంది!';

    final exercises = [
      {
        'q_en': 'What energy powers the little plant kitchen?',
        'q_te': 'మొక్కల చిన్న వంటగదికి అవసరమైన శక్తి ఎక్కడి నుండి వస్తుంది?',
        'options_en': ['Sunlight (సూర్యరశ్మి)', 'Batteries', 'Wind only', 'Gas Stove'],
        'options_te': ['సూర్యరశ్మి (Sunlight)', 'బ్యాటరీలు', 'గాలి మాత్రమే', 'గ్యాస్ పొయ్యి'],
        'correct': 0,
        'hint_en': 'It comes down from the sky every sunny morning!',
        'hint_te': 'ప్రతి ఉదయం ఆకాశం నుండి వెలుగు రూపంలో వస్తుంది!',
      },
      {
        'q_en': 'Which fresh breath of air do plants share with animals?',
        'q_te': 'మొక్కలు జంతువులకు, మానవులకు అందించే ప్రాణవాయువు ఏది?',
        'options_en': ['Oxygen (O₂)', 'Smoke', 'Dust', 'Carbon Monoxide'],
        'options_te': ['ఆక్సిజన్ (O₂)', 'పొగ', 'ధూళి', 'కార్బన్ మోనాక్సైడ్'],
        'correct': 0,
        'hint_en': 'The wonderful gas that fills our lungs when we run!',
        'hint_te': 'మనం బ్రతకడానికి పీల్చుకునే ప్రాణవాయువు!',
      },
    ];

    final currentEx = exercises[_currentStep];
    final options = lang == 'te' ? currentEx['options_te'] as List<String> : currentEx['options_en'] as List<String>;
    final question = lang == 'te' ? currentEx['q_te'] as String : currentEx['q_en'] as String;
    final hint = lang == 'te' ? currentEx['hint_te'] as String : currentEx['hint_en'] as String;

    return Scaffold(
      backgroundColor: AppColors.softBackground,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        title: Text(
          lang == 'te' ? 'వ్యక్తిగతీకరించిన సాధన 💡' : 'Personalized Practice 💡',
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
                    // Bala Buddy Encouragement Header
                    Container(
                      padding: const EdgeInsets.all(16.0),
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          colors: [Color(0xFFFFF9C4), Color(0xFFFFF176)],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: Colors.amber, width: 1.5),
                      ),
                      child: Row(
                        children: [
                          const Text('🤖', style: TextStyle(fontSize: 34)),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  lang == 'te' ? 'బాల బడ్డీ సహాయం సిద్ధం! 🌟' : 'Bala Buddy is here to help! 🌟',
                                  style: const TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.bold,
                                    color: Color(0xFF5D4037),
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  lang == 'te'
                                      ? 'తప్పులు చేయడం సాధారణం! ఈ సులువైన ఉదాహరణతో భావనను నేర్చుకుందాం.'
                                      : 'Making mistakes makes our brain stronger! Let\'s master this with a simple story.',
                                  style: const TextStyle(fontSize: 13, color: Color(0xFF5D4037)),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),

                    // Simplified Analogy Card
                    Container(
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
                              const Text('💡', style: TextStyle(fontSize: 22)),
                              const SizedBox(width: 8),
                              Text(
                                lang == 'te' ? 'సులభమైన వివరణ (Simple Analogy):' : 'Easy Concept Analogy:',
                                style: const TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                  color: AppColors.primaryBlue,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 10),
                          Text(
                            lang == 'te' ? simplifiedExplanationTe : simplifiedExplanationEn,
                            style: const TextStyle(fontSize: 15, height: 1.5, color: AppColors.textDark),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),

                    // Booster Exercise Card
                    Container(
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
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                decoration: BoxDecoration(
                                  color: AppColors.lightOrange,
                                  borderRadius: BorderRadius.circular(10),
                                ),
                                child: Text(
                                  'Booster Exercise ${_currentStep + 1} / ${exercises.length}',
                                  style: const TextStyle(
                                    fontSize: 12,
                                    fontWeight: FontWeight.bold,
                                    color: AppColors.coralOrange,
                                  ),
                                ),
                              ),
                              const Spacer(),
                              Text('+$_bonusXpEarned XP ⚡',
                                  style: const TextStyle(fontWeight: FontWeight.bold, color: AppColors.darkGreen)),
                            ],
                          ),
                          const SizedBox(height: 12),
                          Text(
                            question,
                            style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: AppColors.textDark),
                          ),
                          const SizedBox(height: 14),

                          // Options
                          ...List.generate(options.length, (idx) {
                            final isSelected = _selectedOption == idx;
                            Color borderCol = AppColors.borderColor;
                            Color bgCol = Colors.white;

                            if (_submitted) {
                              if (idx == currentEx['correct']) {
                                borderCol = AppColors.meadowGreen;
                                bgCol = AppColors.lightGreen;
                              } else if (isSelected) {
                                borderCol = Colors.red;
                                bgCol = const Color(0xFFFFEBEE);
                              }
                            } else if (isSelected) {
                              borderCol = AppColors.primaryBlue;
                              bgCol = AppColors.lightBlue;
                            }

                            return Container(
                              margin: const EdgeInsets.only(bottom: 10),
                              constraints: const BoxConstraints(minHeight: 50),
                              child: Material(
                                color: bgCol,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(14),
                                  side: BorderSide(color: borderCol, width: 2),
                                ),
                                child: InkWell(
                                  borderRadius: BorderRadius.circular(14),
                                  onTap: _submitted ? null : () => setState(() => _selectedOption = idx),
                                  child: Padding(
                                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                                    child: Row(
                                      children: [
                                        Text(String.fromCharCode(65 + idx),
                                            style: const TextStyle(fontWeight: FontWeight.bold)),
                                        const SizedBox(width: 12),
                                        Expanded(child: Text(options[idx])),
                                        if (_submitted && idx == currentEx['correct'])
                                          const Icon(Icons.check_circle_rounded, color: AppColors.meadowGreen),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                            );
                          }),

                          if (_submitted) ...[
                            const SizedBox(height: 8),
                            Text('💡 $hint', style: const TextStyle(color: AppColors.textMuted, fontSize: 13)),
                            const SizedBox(height: 12),
                            ElevatedButton(
                              style: ElevatedButton.styleFrom(
                                backgroundColor: AppColors.primaryBlue,
                                foregroundColor: Colors.white,
                                minimumSize: const Size(double.infinity, 48),
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                              ),
                              onPressed: () {
                                if (_currentStep + 1 < exercises.length) {
                                  setState(() {
                                    _currentStep++;
                                    _selectedOption = null;
                                    _submitted = false;
                                  });
                                } else {
                                  Navigator.of(context).pop();
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    SnackBar(
                                      content: Text(
                                        lang == 'te'
                                            ? 'అభినందనలు! ప్రత్యేక సాధన పూర్తి చేసి 20 XP సంపాదించారు! 🌟'
                                            : 'Great job! You finished personalized practice and earned 20 XP! 🌟',
                                      ),
                                    ),
                                  );
                                }
                              },
                              child: Text(
                                _currentStep + 1 < exercises.length ? 'Next Exercise' : 'Finish Practice 🌟',
                                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                              ),
                            ),
                          ] else ...[
                            const SizedBox(height: 8),
                            ElevatedButton(
                              style: ElevatedButton.styleFrom(
                                backgroundColor: AppColors.meadowGreen,
                                foregroundColor: Colors.white,
                                minimumSize: const Size(double.infinity, 48),
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                              ),
                              onPressed: _selectedOption == null
                                  ? null
                                  : () {
                                      setState(() {
                                        _submitted = true;
                                        if (_selectedOption == currentEx['correct']) {
                                          _bonusXpEarned += 10;
                                          ref.read(learnerXpProvider.notifier).state += 10;
                                          ref.read(learnerCoinsProvider.notifier).state += 2;
                                          SyncQueueService().enqueueEvent(
                                            learnerId: ref.read(currentLearnerIdProvider),
                                            eventType: 'personalized_practice_completed',
                                            payload: {'topic_id': widget.topicId, 'step': _currentStep},
                                          );
                                        }
                                      });
                                    },
                              child: Text(
                                AppStrings.get('checkAnswer', lang),
                                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                              ),
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

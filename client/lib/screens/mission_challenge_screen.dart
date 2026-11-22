import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/models/chapter_package_model.dart';
import 'package:baalavidya/services/offline_store.dart';
import 'package:baalavidya/services/sync_queue_service.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';
import 'package:baalavidya/widgets/certificate_widget.dart';
import 'package:baalavidya/widgets/language_toggle.dart';
import 'package:baalavidya/widgets/offline_banner.dart';

/// End-of-Chapter Mission Challenge Screen [PS: 11. End-of-Chapter Challenge].
/// Combines Quiz + Puzzle + Scenario + Mini Game.
/// Rewards: Chapter Badge, +50 XP bonus, and Achievement Certificate.
class MissionChallengeScreen extends ConsumerStatefulWidget {
  final String chapterId;

  const MissionChallengeScreen({
    super.key,
    this.chapterId = 'bio_ch1',
  });

  @override
  ConsumerState<MissionChallengeScreen> createState() => _MissionChallengeScreenState();
}

class _MissionChallengeScreenState extends ConsumerState<MissionChallengeScreen> {
  int _stage = 0; // 0: Quiz, 1: Puzzle, 2: Scenario, 3: Completed

  // Stage 0: Quiz
  int? _selectedQuizOption;

  // Stage 1: Puzzle
  String? _selectedPuzzlePiece;

  // Stage 2: Scenario
  int? _selectedScenarioOption;

  bool _isSuccess = false;

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);
    final pkg = OfflineStore().getChapterPackage(widget.chapterId);
    final mission = pkg?.missionChallenge;

    if (mission == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('Mission Challenge')),
        body: const Center(child: Text('No mission challenge configured for this chapter.')),
      );
    }

    return Scaffold(
      backgroundColor: AppColors.softBackground,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        title: Text(
          mission.localizedTitle(lang),
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
                child: _stage == 3
                    ? _buildVictoryCard(mission, lang)
                    : Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // Mission Progress Bar
                          Row(
                            children: [
                              _buildStageIndicator(0, '1. Quiz 📝', _stage >= 0),
                              const SizedBox(width: 6),
                              _buildStageIndicator(1, '2. Puzzle 🧩', _stage >= 1),
                              const SizedBox(width: 6),
                              _buildStageIndicator(2, '3. Scenario 🌿', _stage >= 2),
                            ],
                          ),
                          const SizedBox(height: 18),

                          if (_stage == 0) _buildQuizStage(mission, lang),
                          if (_stage == 1) _buildPuzzleStage(mission, lang),
                          if (_stage == 2) _buildScenarioStage(mission, lang),
                        ],
                      ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStageIndicator(int index, String title, bool active) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 8),
        decoration: BoxDecoration(
          color: active ? AppColors.primaryBlue : Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: active ? AppColors.primaryBlue : AppColors.borderColor),
        ),
        alignment: Alignment.center,
        child: Text(
          title,
          style: TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.bold,
            color: active ? Colors.white : AppColors.textMuted,
          ),
        ),
      ),
    );
  }

  Widget _buildQuizStage(MissionChallengeModel mission, String lang) {
    final options = mission.localizedQuizOptions(lang);

    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppColors.borderColor, width: 1.5),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: const [
              Text('🎯 Phase 1: Master Quiz', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              Spacer(),
              Text('+15 XP', style: TextStyle(color: AppColors.meadowGreen, fontWeight: FontWeight.bold)),
            ],
          ),
          const SizedBox(height: 14),
          Text(
            mission.localizedQuizQuestion(lang),
            style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: AppColors.textDark),
          ),
          const SizedBox(height: 16),
          ...List.generate(options.length, (idx) {
            final isSelected = _selectedQuizOption == idx;
            return Container(
              margin: const EdgeInsets.only(bottom: 10),
              child: Material(
                color: isSelected ? AppColors.lightBlue : Colors.white,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(14),
                  side: BorderSide(
                    color: isSelected ? AppColors.primaryBlue : AppColors.borderColor,
                    width: 2,
                  ),
                ),
                child: InkWell(
                  borderRadius: BorderRadius.circular(14),
                  onTap: () => setState(() => _selectedQuizOption = idx),
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                    child: Text(options[idx], style: const TextStyle(fontSize: 16)),
                  ),
                ),
              ),
            );
          }),
          const SizedBox(height: 14),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primaryBlue,
              foregroundColor: Colors.white,
              minimumSize: const Size(double.infinity, 50),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
            ),
            onPressed: _selectedQuizOption == null
                ? null
                : () {
                    if (_selectedQuizOption == mission.correctQuizIndex) {
                      setState(() => _stage = 1);
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Try again! 12 water molecules are split by light.')),
                      );
                    }
                  },
            child: const Text('Next to Puzzle 🧩', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }

  Widget _buildPuzzleStage(MissionChallengeModel mission, String lang) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppColors.borderColor, width: 1.5),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: const [
              Text('🧩 Phase 2: Word Puzzle', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              Spacer(),
              Text('+15 XP', style: TextStyle(color: AppColors.meadowGreen, fontWeight: FontWeight.bold)),
            ],
          ),
          const SizedBox(height: 14),
          Text(
            mission.localizedPuzzlePrompt(lang),
            style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: AppColors.textDark),
          ),
          const SizedBox(height: 16),
          Wrap(
            spacing: 10,
            runSpacing: 10,
            children: mission.puzzlePieces.map((piece) {
              final isSel = _selectedPuzzlePiece == piece;
              return ChoiceChip(
                label: Text(piece, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
                selected: isSel,
                selectedColor: AppColors.sunshineYellow,
                backgroundColor: AppColors.softBackground,
                onSelected: (val) => setState(() => _selectedPuzzlePiece = val ? piece : null),
              );
            }).toList(),
          ),
          const SizedBox(height: 20),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.candyPurple,
              foregroundColor: Colors.white,
              minimumSize: const Size(double.infinity, 50),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
            ),
            onPressed: _selectedPuzzlePiece == null
                ? null
                : () {
                    if (_selectedPuzzlePiece == 'CHLOROPHYLL') {
                      setState(() => _stage = 2);
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Unscramble: C-H-L-O-R-O-P-H-Y-L-L!')),
                      );
                    }
                  },
            child: const Text('Next to Scenario 🌿', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }

  Widget _buildScenarioStage(MissionChallengeModel mission, String lang) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppColors.borderColor, width: 1.5),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: const [
              Text('🌿 Phase 3: Real Scenario', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              Spacer(),
              Text('+20 XP', style: TextStyle(color: AppColors.meadowGreen, fontWeight: FontWeight.bold)),
            ],
          ),
          const SizedBox(height: 14),
          Text(
            mission.localizedScenarioQuestion(lang),
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppColors.textDark, height: 1.4),
          ),
          const SizedBox(height: 16),
          ...List.generate(mission.scenarioOptions.length, (idx) {
            final isSelected = _selectedScenarioOption == idx;
            return Container(
              margin: const EdgeInsets.only(bottom: 10),
              child: Material(
                color: isSelected ? AppColors.lightGreen : Colors.white,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(14),
                  side: BorderSide(
                    color: isSelected ? AppColors.meadowGreen : AppColors.borderColor,
                    width: 2,
                  ),
                ),
                child: InkWell(
                  borderRadius: BorderRadius.circular(14),
                  onTap: () => setState(() => _selectedScenarioOption = idx),
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                    child: Text(mission.scenarioOptions[idx], style: const TextStyle(fontSize: 15)),
                  ),
                ),
              ),
            );
          }),
          const SizedBox(height: 16),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.coralOrange,
              foregroundColor: Colors.white,
              minimumSize: const Size(double.infinity, 50),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
            ),
            onPressed: _selectedScenarioOption == null
                ? null
                : () {
                    if (_selectedScenarioOption == mission.correctScenarioIndex) {
                      _finishMission(mission);
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Without light, plants cannot synthesize starch!')),
                      );
                    }
                  },
            child: const Text('Complete Mission! 🏆', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }

  void _finishMission(MissionChallengeModel mission) {
    setState(() {
      _stage = 3;
      _isSuccess = true;
    });

    // 1. Award +50 XP bonus, +25 Coins, and 3 Stars
    ref.read(learnerXpProvider.notifier).state += 50;
    ref.read(learnerCoinsProvider.notifier).state += 25;
    ref.read(learnerStarsProvider.notifier).state += 3;

    // 2. Award Chapter Mission Badge
    ref.read(learnerBadgesProvider.notifier).update((badges) => {...badges, 'mission_master'});

    // 3. Generate Achievement Certificate
    final cert = CertificateModel(
      certificateId: 'CERT-${widget.chapterId.toUpperCase()}-MISSION',
      learnerName: ref.read(currentLearnerNameProvider),
      chapterTitle: 'Nutrition - Food Supplying System',
      teluguChapterTitle: 'పోషణ - ఆహార సరఫరా వ్యవస్థ',
      subjectName: 'Biology (జీవశాస్త్రం)',
      issueDate: '22 November 2026',
      scorePercentage: 100,
      badgeName: 'Mission Champion 🏅',
    );
    OfflineStore().saveCertificate(cert);
    ref.read(certificatesProvider.notifier).state = OfflineStore().getCertificates();

    // 4. Enqueue Sync Event (Sync Rule 1: write locally first)
    SyncQueueService().enqueueEvent(
      learnerId: ref.read(currentLearnerIdProvider),
      eventType: 'mission_completed',
      payload: {
        'chapter_id': widget.chapterId,
        'bonus_xp': 50,
        'badge': 'mission_master',
      },
    );
  }

  Widget _buildVictoryCard(MissionChallengeModel mission, String lang) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: AppColors.sunshineYellow, width: 2),
      ),
      child: Column(
        children: [
          const Text('🏆', style: TextStyle(fontSize: 60)),
          const SizedBox(height: 12),
          Text(
            lang == 'te' ? 'మిషన్ విజయవంతమైంది! 🌟' : 'MISSION ACCOMPLISHED! 🌟',
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: AppColors.darkBlue),
          ),
          const SizedBox(height: 10),
          Text(
            lang == 'te'
                ? 'మీరు చాప్టర్ మిషన్‌ను అద్భుతంగా పూర్తి చేసి 50 XP & మిషన్ బ్యాడ్జ్ గెలుచుకున్నారు!'
                : 'You mastered the chapter mission challenge and unlocked your Official Certificate!',
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 15, color: AppColors.textDark, height: 1.4),
          ),
          const SizedBox(height: 18),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
            decoration: BoxDecoration(
              color: AppColors.lightYellow,
              borderRadius: BorderRadius.circular(16),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: const [
                Text('🏅 Mission Master Badge Earned! • +50 XP ⚡',
                    style: TextStyle(fontWeight: FontWeight.bold, color: AppColors.textDark)),
              ],
            ),
          ),
          const SizedBox(height: 24),
          ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primaryBlue,
              foregroundColor: Colors.white,
              minimumSize: const Size(double.infinity, 50),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
            ),
            icon: const Text('📜', style: TextStyle(fontSize: 20)),
            label: Text(
              lang == 'te' ? 'సర్టిఫికేట్ చూడండి' : 'View Achievement Certificate',
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            onPressed: () {
              final certs = OfflineStore().getCertificates();
              if (certs.isNotEmpty) {
                CertificateWidget.showCertificateDialog(context, certs.last);
              }
            },
          ),
        ],
      ),
    );
  }
}

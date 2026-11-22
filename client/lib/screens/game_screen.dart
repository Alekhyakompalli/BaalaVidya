import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/models/chapter_package_model.dart';
import 'package:baalavidya/services/offline_store.dart';
import 'package:baalavidya/services/sync_queue_service.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';
import 'package:baalavidya/widgets/language_toggle.dart';
import 'package:baalavidya/widgets/offline_banner.dart';

/// Interactive Educational Games screen across 5 Subjects.
/// Adheres to:
/// - [PS: 11. Learning Games (Mathematics, Science, Social Studies, English, Telugu)]
/// - [PS: Offline Compatibility].
class GameScreen extends ConsumerStatefulWidget {
  final String chapterId;

  const GameScreen({
    super.key,
    this.chapterId = 'bio_ch1',
  });

  @override
  ConsumerState<GameScreen> createState() => _GameScreenState();
}

class _GameScreenState extends ConsumerState<GameScreen> {
  String _selectedSubject = 'biology'; // 'biology', 'mathematics', 'social_studies', 'english', 'telugu'
  final Set<int> _matchedPairs = {};
  int? _selectedSourceIndex;

  void _switchSubject(String subj) {
    setState(() {
      _selectedSubject = subj;
      _matchedPairs.clear();
      _selectedSourceIndex = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);
    final allGames = OfflineStore().getAllEducationalGames();

    // Filter games for current subject or fallback to first
    final gamesForSubj = allGames.where((g) => g.subjectId == _selectedSubject).toList();
    final game = gamesForSubj.isNotEmpty ? gamesForSubj.first : allGames.firstOrNull;

    if (game == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('Educational Game')),
        body: const Center(child: Text('No game available.')),
      );
    }

    final pairs = game.pairs;
    final isGameCompleted = _matchedPairs.length == pairs.length;

    return Scaffold(
      backgroundColor: AppColors.softBackground,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        title: Text(
          game.localizedTitle(lang),
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

            // Subject Game Tabs (Math, Science, Social, English, Telugu) [PS: 11. Learning Games]
            Container(
              color: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: [
                    _buildSubjTab('biology', 'Science 🔬', 'సైన్స్ 🔬', lang),
                    const SizedBox(width: 8),
                    _buildSubjTab('mathematics', 'Math 📐', 'గణితం 📐', lang),
                    const SizedBox(width: 8),
                    _buildSubjTab('social_studies', 'Social 🌍', 'సాంఘిక 🌍', lang),
                    const SizedBox(width: 8),
                    _buildSubjTab('english', 'English 📚', 'ఇంగ్లీష్ 📚', lang),
                    const SizedBox(width: 8),
                    _buildSubjTab('telugu', 'Telugu 📖', 'తెలుగు 📖', lang),
                  ],
                ),
              ),
            ),
            const Divider(height: 1, color: AppColors.borderColor),

            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    // Game Instructions Banner
                    Container(
                      padding: const EdgeInsets.all(14.0),
                      decoration: BoxDecoration(
                        color: AppColors.lightPurple,
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: AppColors.candyPurple.withOpacity(0.3)),
                      ),
                      child: Row(
                        children: [
                          const Text('🎮', style: TextStyle(fontSize: 28)),
                          const SizedBox(width: 10),
                          Expanded(
                            child: Text(
                              game.localizedDescription(lang).isNotEmpty
                                  ? game.localizedDescription(lang)
                                  : (lang == 'te'
                                      ? 'ఎడమ వైపు భాగాన్ని ఎంచుకుని, కుడి వైపు సరైన సమాధానంతో జతపరచండి!'
                                      : 'Tap an item on the left, then connect it to its match on the right!'),
                              style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: AppColors.textDark),
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),

                    // Matching Game Grid / Column
                    ListView.builder(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      itemCount: pairs.length,
                      itemBuilder: (context, idx) {
                        final isMatched = _matchedPairs.contains(idx);
                        final isSelected = _selectedSourceIndex == idx;

                        return Container(
                          margin: const EdgeInsets.only(bottom: 12),
                          child: Row(
                            children: [
                              // Source item
                              Expanded(
                                child: Container(
                                  constraints: const BoxConstraints(minHeight: 52),
                                  child: Material(
                                    color: isMatched
                                        ? AppColors.lightGreen
                                        : (isSelected ? AppColors.lightBlue : Colors.white),
                                    shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(14),
                                      side: BorderSide(
                                        color: isMatched
                                            ? AppColors.meadowGreen
                                            : (isSelected ? AppColors.primaryBlue : AppColors.borderColor),
                                        width: 2,
                                      ),
                                    ),
                                    child: InkWell(
                                      borderRadius: BorderRadius.circular(14),
                                      onTap: isMatched
                                          ? null
                                          : () {
                                              setState(() => _selectedSourceIndex = idx);
                                            },
                                      child: Padding(
                                        padding: const EdgeInsets.all(12.0),
                                        child: Text(
                                          pairs[idx].source,
                                          style: TextStyle(
                                            fontSize: 14,
                                            fontWeight: FontWeight.bold,
                                            color: isMatched ? AppColors.darkGreen : AppColors.textDark,
                                          ),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              const SizedBox(width: 10),
                              const Icon(Icons.compare_arrows_rounded, color: AppColors.textMuted),
                              const SizedBox(width: 10),

                              // Target item
                              Expanded(
                                child: Container(
                                  constraints: const BoxConstraints(minHeight: 52),
                                  child: Material(
                                    color: isMatched ? AppColors.lightGreen : Colors.white,
                                    shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(14),
                                      side: BorderSide(
                                        color: isMatched ? AppColors.meadowGreen : AppColors.borderColor,
                                        width: 2,
                                      ),
                                    ),
                                    child: InkWell(
                                      borderRadius: BorderRadius.circular(14),
                                      onTap: isMatched || _selectedSourceIndex == null
                                          ? null
                                          : () {
                                              if (_selectedSourceIndex == idx) {
                                                setState(() {
                                                  _matchedPairs.add(idx);
                                                  _selectedSourceIndex = null;
                                                });

                                                if (_matchedPairs.length == pairs.length) {
                                                  ref.read(learnerXpProvider.notifier).state += 30;
                                                  ref.read(learnerCoinsProvider.notifier).state += 10;
                                                  SyncQueueService().enqueueEvent(
                                                    learnerId: ref.read(currentLearnerIdProvider),
                                                    eventType: 'game_played',
                                                    payload: {
                                                      'game_id': game.gameId,
                                                      'subject_id': game.subjectId,
                                                      'status': 'completed'
                                                    },
                                                  );
                                                }
                                              } else {
                                                ScaffoldMessenger.of(context).showSnackBar(
                                                  SnackBar(
                                                    content: Text(
                                                      lang == 'te'
                                                          ? 'తప్పు జత! మరలా ప్రయత్నించండి.'
                                                          : 'Not a match! Try again.',
                                                    ),
                                                    duration: const Duration(seconds: 1),
                                                  ),
                                                );
                                                setState(() => _selectedSourceIndex = null);
                                              }
                                            },
                                      child: Padding(
                                        padding: const EdgeInsets.all(12.0),
                                        child: Text(
                                          pairs[idx].target,
                                          style: TextStyle(
                                            fontSize: 14,
                                            fontWeight: FontWeight.bold,
                                            color: isMatched ? AppColors.darkGreen : AppColors.textDark,
                                          ),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        );
                      },
                    ),

                    // Completion Banner
                    if (isGameCompleted) ...[
                      const SizedBox(height: 18),
                      Container(
                        padding: const EdgeInsets.all(16.0),
                        decoration: BoxDecoration(
                          color: AppColors.lightGreen,
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: AppColors.meadowGreen, width: 2),
                        ),
                        child: Column(
                          children: [
                            const Text('🌟 🏆 🌟', style: TextStyle(fontSize: 26)),
                            const SizedBox(height: 6),
                            Text(
                              lang == 'te'
                                  ? 'అద్భుతం! గేమ్ పూర్తయింది • 30 XP & 10 నాణేలు లభించాయి!'
                                  : 'Awesome! Game Complete! You earned +30 XP & 10 Coins!',
                              textAlign: TextAlign.center,
                              style: const TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: AppColors.darkGreen,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSubjTab(String id, String labelEn, String labelTe, String lang) {
    final isSel = _selectedSubject == id;
    return ChoiceChip(
      label: Text(lang == 'te' ? labelTe : labelEn, style: const TextStyle(fontWeight: FontWeight.bold)),
      selected: isSel,
      selectedColor: AppColors.sunshineYellow,
      backgroundColor: Colors.white,
      onSelected: (val) {
        if (val) _switchSubject(id);
      },
    );
  }
}

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/models/chapter_package_model.dart';
import 'package:baalavidya/screens/personalized_practice_screen.dart';
import 'package:baalavidya/services/offline_store.dart';
import 'package:baalavidya/services/sync_queue_service.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';
import 'package:baalavidya/widgets/language_toggle.dart';
import 'package:baalavidya/widgets/offline_banner.dart';

/// Interactive Practice Workbook screen.
/// Adheres to [PS: 11. Smart Workbook; Offline Compatibility].
/// Supports all 6 activity types 100% offline:
/// 1. MCQ
/// 2. Fill in the blanks (tap-in word bank chips)
/// 3. Match the following
/// 4. True or False
/// 5. Drag and Drop
/// 6. Picture-based questions
class WorkbookScreen extends ConsumerStatefulWidget {
  final String chapterId;

  const WorkbookScreen({
    super.key,
    this.chapterId = 'bio_ch1',
  });

  @override
  ConsumerState<WorkbookScreen> createState() => _WorkbookScreenState();
}

class _WorkbookScreenState extends ConsumerState<WorkbookScreen> {
  int _currentIndex = 0;
  bool _submitted = false;
  int _score = 0;

  // Type-specific state:
  int? _selectedOption; // For MCQ & Picture-based
  String? _selectedBlankWord; // For Fill in the blanks
  bool? _selectedTrueFalse; // For True/False
  String? _droppedWord; // For Drag and drop
  final Set<int> _matchedIndices = {}; // For Match the following
  int? _activeMatchSource;

  void _resetCurrentState() {
    _submitted = false;
    _selectedOption = null;
    _selectedBlankWord = null;
    _selectedTrueFalse = null;
    _droppedWord = null;
    _matchedIndices.clear();
    _activeMatchSource = null;
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);
    final pkg = OfflineStore().getChapterPackage(widget.chapterId);
    var activities = pkg?.workbookActivities ?? [];
    if (activities.isEmpty) {
      activities = OfflineStore().getChapterPackage('bio_ch1')?.workbookActivities ?? [];
    }

    if (activities.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: const Text('Workbook')),
        body: const Center(child: Text('No workbook activities available.')),
      );
    }

    final currentAct = activities[_currentIndex];

    return Scaffold(
      backgroundColor: AppColors.softBackground,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        title: Text(
          lang == 'te' ? 'స్మార్ట్ ప్రాక్టీస్ వర్క్‌బుక్' : 'Smart Practice Workbook',
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
                    // Progress & Score Header
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                          decoration: BoxDecoration(
                            color: AppColors.lightOrange,
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Text(
                            lang == 'te'
                                ? 'ప్రశ్న ${_currentIndex + 1} / ${activities.length}'
                                : 'Question ${_currentIndex + 1} of ${activities.length}',
                            style: const TextStyle(
                              fontSize: 14,
                              fontWeight: FontWeight.bold,
                              color: AppColors.coralOrange,
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            color: AppColors.lightBlue,
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: Text(
                            _getTypeBadge(currentAct.activityType, lang),
                            style: const TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                              color: AppColors.primaryBlue,
                            ),
                          ),
                        ),
                        const Spacer(),
                        Text(
                          'Score: $_score ⭐',
                          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppColors.darkBlue),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),

                    // Question Card
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(18.0),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: AppColors.borderColor, width: 1.5),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.04),
                            blurRadius: 6,
                            offset: const Offset(0, 2),
                          ),
                        ],
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            currentAct.localizedQuestion(lang),
                            style: const TextStyle(
                              fontSize: 17,
                              fontWeight: FontWeight.bold,
                              color: AppColors.textDark,
                              height: 1.35,
                            ),
                          ),
                          const SizedBox(height: 18),

                          // Render UI depending on 1 of the 6 activity types
                          _buildActivityContent(currentAct, lang),

                          // Explanation card after submission
                          if (_submitted) ...[
                            const SizedBox(height: 16),
                            Container(
                              padding: const EdgeInsets.all(14.0),
                              decoration: BoxDecoration(
                                color: AppColors.lightYellow,
                                borderRadius: BorderRadius.circular(14),
                                border: Border.all(color: AppColors.sunshineYellow),
                              ),
                              child: Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Text('💡', style: TextStyle(fontSize: 22)),
                                  const SizedBox(width: 10),
                                  Expanded(
                                    child: Text(
                                      currentAct.localizedExplanation(lang),
                                      style: const TextStyle(
                                        fontSize: 14,
                                        color: AppColors.textDark,
                                        height: 1.4,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                    const SizedBox(height: 20),

                    // Submit / Next Question Action Button
                    if (!_submitted)
                      ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.meadowGreen,
                          foregroundColor: Colors.white,
                          minimumSize: const Size(double.infinity, 52),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                        ),
                        onPressed: _canSubmit(currentAct) ? () => _submitAnswer(currentAct) : null,
                        child: Text(
                          lang == 'te' ? 'సరిచూసుకోండి' : 'Check Answer',
                          style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold),
                        ),
                      )
                    else
                      ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.primaryBlue,
                          foregroundColor: Colors.white,
                          minimumSize: const Size(double.infinity, 52),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                        ),
                        onPressed: () {
                          if (_currentIndex + 1 < activities.length) {
                            setState(() {
                              _currentIndex++;
                              _resetCurrentState();
                            });
                          } else {
                            _showCompletionDialog(activities.length, lang);
                          }
                        },
                        child: Text(
                          _currentIndex + 1 < activities.length
                              ? (lang == 'te' ? 'తర్వాతి ప్రశ్న ➔' : 'Next Question ➔')
                              : (lang == 'te' ? 'వర్క్‌బుక్ ముగించు 🌟' : 'Finish Workbook 🌟'),
                          style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold),
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

  String _getTypeBadge(String type, String lang) {
    if (lang == 'te') {
      switch (type) {
        case 'fill_blank':
          return 'ఖాళీలు పూరించండి';
        case 'match':
          return 'జతపరచండి';
        case 'true_false':
          return 'సత్యం / అసత్యం';
        case 'drag_drop':
          return 'డ్రాగ్ & డ్రాప్';
        case 'picture_based':
          return 'పటం ఆధారిత ప్రశ్న';
        default:
          return 'బహుళైచ్ఛిక ప్రశ్న';
      }
    }
    switch (type) {
      case 'fill_blank':
        return 'Fill in Blanks';
      case 'match':
        return 'Match Following';
      case 'true_false':
        return 'True / False';
      case 'drag_drop':
        return 'Drag & Drop';
      case 'picture_based':
        return 'Picture-based';
      default:
        return 'Multiple Choice';
    }
  }

  bool _canSubmit(WorkbookActivity act) {
    switch (act.activityType) {
      case 'fill_blank':
        return _selectedBlankWord != null;
      case 'match':
        return _matchedIndices.length == act.matchPairs.length;
      case 'true_false':
        return _selectedTrueFalse != null;
      case 'drag_drop':
        return _droppedWord != null;
      case 'picture_based':
      case 'mcq':
      default:
        return _selectedOption != null;
    }
  }

  void _submitAnswer(WorkbookActivity act) {
    bool correct = false;
    switch (act.activityType) {
      case 'fill_blank':
        correct = _selectedBlankWord == act.correctAnswer || _selectedBlankWord == act.teluguCorrectAnswer;
        break;
      case 'match':
        correct = _matchedIndices.length == act.matchPairs.length;
        break;
      case 'true_false':
        correct = _selectedTrueFalse == act.isTrue;
        break;
      case 'drag_drop':
        correct = _droppedWord == act.correctAnswer || _droppedWord == act.teluguCorrectAnswer;
        break;
      case 'picture_based':
      case 'mcq':
      default:
        correct = _selectedOption == act.correctIndex;
        break;
    }

    setState(() {
      _submitted = true;
      if (correct) {
        _score += 10;
        ref.read(learnerXpProvider.notifier).state += 10;
        ref.read(learnerCoinsProvider.notifier).state += 2;
      }
    });

    // Write progress locally to sync queue
    SyncQueueService().enqueueEvent(
      learnerId: ref.read(currentLearnerIdProvider),
      eventType: 'workbook_item_answered',
      payload: {
        'activity_id': act.activityId,
        'activity_type': act.activityType,
        'correct': correct,
      },
    );
  }

  Widget _buildActivityContent(WorkbookActivity act, String lang) {
    switch (act.activityType) {
      case 'fill_blank':
        return _buildFillBlank(act, lang);
      case 'match':
        return _buildMatch(act, lang);
      case 'true_false':
        return _buildTrueFalse(act, lang);
      case 'drag_drop':
        return _buildDragDrop(act, lang);
      case 'picture_based':
        return _buildPictureBased(act, lang);
      case 'mcq':
      default:
        return _buildMcq(act, lang);
    }
  }

  // 1. MCQ
  Widget _buildMcq(WorkbookActivity act, String lang) {
    final options = act.localizedOptions(lang);
    return Column(
      children: List.generate(options.length, (idx) {
        final isSelected = _selectedOption == idx;
        Color borderCol = AppColors.borderColor;
        Color bgCol = Colors.white;

        if (_submitted) {
          if (idx == act.correctIndex) {
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
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                child: Row(
                  children: [
                    Text(String.fromCharCode(65 + idx), style: const TextStyle(fontWeight: FontWeight.bold)),
                    const SizedBox(width: 12),
                    Expanded(child: Text(options[idx])),
                    if (_submitted && idx == act.correctIndex)
                      const Icon(Icons.check_circle_rounded, color: AppColors.meadowGreen),
                    if (_submitted && isSelected && idx != act.correctIndex)
                      const Icon(Icons.cancel_rounded, color: Colors.red),
                  ],
                ),
              ),
            ),
          ),
        );
      }),
    );
  }

  // 2. Fill in the Blanks (with tap-friendly word bank chips)
  Widget _buildFillBlank(WorkbookActivity act, String lang) {
    final sentence = act.localizedBlankSentence(lang);
    final wordBank = act.localizedWordBank(lang);
    final displayedWord = _selectedBlankWord ?? '________';

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: AppColors.lightBlue,
            borderRadius: BorderRadius.circular(16),
          ),
          child: Text(
            sentence.replaceAll('[BLANK]', displayedWord),
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, height: 1.5),
          ),
        ),
        const SizedBox(height: 16),
        Text(
          lang == 'te' ? 'సరైన పదాన్ని ట్యాప్ చేయండి:' : 'Tap a word from the bank below:',
          style: const TextStyle(fontSize: 13, color: AppColors.textMuted),
        ),
        const SizedBox(height: 8),
        Wrap(
          spacing: 10,
          runSpacing: 10,
          children: wordBank.map((w) {
            final isSel = _selectedBlankWord == w;
            return ActionChip(
              label: Text(w, style: const TextStyle(fontWeight: FontWeight.bold)),
              backgroundColor: isSel ? AppColors.primaryBlue : Colors.white,
              labelStyle: TextStyle(color: isSel ? Colors.white : AppColors.textDark),
              onPressed: _submitted ? null : () => setState(() => _selectedBlankWord = w),
            );
          }).toList(),
        ),
      ],
    );
  }

  // 3. Match the Following
  Widget _buildMatch(WorkbookActivity act, String lang) {
    final pairs = act.matchPairs;
    return Column(
      children: List.generate(pairs.length, (idx) {
        final isMatched = _matchedIndices.contains(idx);
        final isSelected = _activeMatchSource == idx;

        return Container(
          margin: const EdgeInsets.only(bottom: 10),
          child: Row(
            children: [
              Expanded(
                child: Material(
                  color: isMatched ? AppColors.lightGreen : (isSelected ? AppColors.lightBlue : Colors.white),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                    side: BorderSide(
                      color: isMatched
                          ? AppColors.meadowGreen
                          : (isSelected ? AppColors.primaryBlue : AppColors.borderColor),
                      width: 2,
                    ),
                  ),
                  child: InkWell(
                    borderRadius: BorderRadius.circular(12),
                    onTap: isMatched ? null : () => setState(() => _activeMatchSource = idx),
                    child: Padding(
                      padding: const EdgeInsets.all(10),
                      child: Text(pairs[idx].source, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                    ),
                  ),
                ),
              ),
              const Padding(
                padding: EdgeInsets.symmetric(horizontal: 6),
                child: Icon(Icons.arrow_forward_rounded, size: 18, color: AppColors.textMuted),
              ),
              Expanded(
                child: Material(
                  color: isMatched ? AppColors.lightGreen : Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                    side: BorderSide(
                      color: isMatched ? AppColors.meadowGreen : AppColors.borderColor,
                      width: 2,
                    ),
                  ),
                  child: InkWell(
                    borderRadius: BorderRadius.circular(12),
                    onTap: isMatched || _activeMatchSource == null
                        ? null
                        : () {
                            if (_activeMatchSource == idx) {
                              setState(() {
                                _matchedIndices.add(idx);
                                _activeMatchSource = null;
                              });
                            } else {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(content: Text('Not a match! Try another pair.')),
                              );
                              setState(() => _activeMatchSource = null);
                            }
                          },
                    child: Padding(
                      padding: const EdgeInsets.all(10),
                      child: Text(pairs[idx].target, style: const TextStyle(fontSize: 13)),
                    ),
                  ),
                ),
              ),
            ],
          ),
        );
      }),
    );
  }

  // 4. True or False
  Widget _buildTrueFalse(WorkbookActivity act, String lang) {
    return Row(
      children: [
        Expanded(
          child: ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              backgroundColor: _selectedTrueFalse == true ? AppColors.meadowGreen : Colors.white,
              foregroundColor: _selectedTrueFalse == true ? Colors.white : AppColors.textDark,
              side: const BorderSide(color: AppColors.meadowGreen, width: 2),
              minimumSize: const Size(0, 52),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
            ),
            icon: const Text('✅', style: TextStyle(fontSize: 20)),
            label: Text(lang == 'te' ? 'సత్యం (True)' : 'True', style: const TextStyle(fontWeight: FontWeight.bold)),
            onPressed: _submitted ? null : () => setState(() => _selectedTrueFalse = true),
          ),
        ),
        const SizedBox(width: 14),
        Expanded(
          child: ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              backgroundColor: _selectedTrueFalse == false ? Colors.red : Colors.white,
              foregroundColor: _selectedTrueFalse == false ? Colors.white : AppColors.textDark,
              side: const BorderSide(color: Colors.red, width: 2),
              minimumSize: const Size(0, 52),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
            ),
            icon: const Text('❌', style: TextStyle(fontSize: 20)),
            label: Text(lang == 'te' ? 'అసత్యం (False)' : 'False', style: const TextStyle(fontWeight: FontWeight.bold)),
            onPressed: _submitted ? null : () => setState(() => _selectedTrueFalse = false),
          ),
        ),
      ],
    );
  }

  // 5. Drag and Drop Activity
  Widget _buildDragDrop(WorkbookActivity act, String lang) {
    final wordBank = act.localizedWordBank(lang);

    return Column(
      children: [
        DragTarget<String>(
          builder: (context, candidateData, rejectedData) {
            final isHovered = candidateData.isNotEmpty;
            return Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
              decoration: BoxDecoration(
                color: isHovered ? AppColors.lightGreen : AppColors.softBackground,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: isHovered ? AppColors.meadowGreen : AppColors.primaryBlue,
                  width: 2,
                  style: BorderStyle.solid,
                ),
              ),
              child: Column(
                children: [
                  const Text('🌿 Plant Solar Factory Slot', style: TextStyle(fontSize: 13, color: AppColors.textMuted)),
                  const SizedBox(height: 8),
                  Text(
                    _droppedWord ?? (lang == 'te' ? 'ఇక్కడికి డ్రాగ్ చేయండి 📥' : 'Drag Answer Card Here 📥'),
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: _droppedWord != null ? AppColors.primaryBlue : AppColors.textMuted,
                    ),
                  ),
                ],
              ),
            );
          },
          onAcceptWithDetails: (details) {
            if (!_submitted) {
              setState(() => _droppedWord = details.data);
            }
          },
        ),
        const SizedBox(height: 16),
        Wrap(
          spacing: 10,
          runSpacing: 10,
          children: wordBank.map((word) {
            return Draggable<String>(
              data: word,
              feedback: Material(
                elevation: 4,
                borderRadius: BorderRadius.circular(12),
                color: AppColors.sunshineYellow,
                child: Padding(
                  padding: const EdgeInsets.all(10),
                  child: Text(word, style: const TextStyle(fontWeight: FontWeight.bold)),
                ),
              ),
              childWhenDragging: Opacity(
                opacity: 0.3,
                child: Chip(label: Text(word)),
              ),
              child: ActionChip(
                label: Text(word, style: const TextStyle(fontWeight: FontWeight.bold)),
                backgroundColor: _droppedWord == word ? AppColors.lightGreen : Colors.white,
                onPressed: _submitted ? null : () => setState(() => _droppedWord = word),
              ),
            );
          }).toList(),
        ),
      ],
    );
  }

  // 6. Picture-Based Question
  Widget _buildPictureBased(WorkbookActivity act, String lang) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Picture Illustration container
        Container(
          width: double.infinity,
          height: 160,
          decoration: BoxDecoration(
            color: const Color(0xFFE8F5E9),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: AppColors.meadowGreen),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text('🍃', style: TextStyle(fontSize: 50)),
              const SizedBox(height: 6),
              Text(
                lang == 'te' ? 'హరితరేణువు అంతర్నిర్మాణం (Chloroplast Anatomy)' : 'Chloroplast Anatomy Diagram',
                style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AppColors.darkGreen),
              ),
              const SizedBox(height: 4),
              const Text(
                'Grana Thylakoids (Disks) • Stroma (Fluid Matrix) • Double Membrane',
                style: TextStyle(fontSize: 11, color: AppColors.textMuted),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        _buildMcq(act, lang),
      ],
    );
  }

  void _showCompletionDialog(int totalQuestions, String lang) {
    final maxScore = totalQuestions * 10;
    final percentage = (totalQuestions > 0 ? (_score / maxScore) : 1.0) * 100;
    final isStruggling = percentage < 60;

    // Award workbook completion bonus XP & coins
    ref.read(learnerXpProvider.notifier).state += 30;
    ref.read(learnerCoinsProvider.notifier).state += 10;
    if (percentage >= 90) {
      ref.read(learnerStarsProvider.notifier).state += 3;
    } else if (percentage >= 70) {
      ref.read(learnerStarsProvider.notifier).state += 2;
    } else {
      ref.read(learnerStarsProvider.notifier).state += 1;
    }

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: Text(
          lang == 'te' ? 'వర్క్‌బుక్ పూర్తయింది! 🌟' : 'Workbook Completed! 🌟',
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('⭐ Score: $_score / $maxScore (${percentage.round()}%) ⭐',
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppColors.primaryBlue)),
            const SizedBox(height: 10),
            Text(
              percentage >= 80
                  ? (lang == 'te' ? 'అద్భుతమైన ప్రతిభ! 30 XP & 10 పాయింట్లు లభించాయి!' : 'Outstanding mastery! Earned +30 XP & 10 Points!')
                  : (lang == 'te' ? 'మంచి ప్రయత్నం! అభ్యాసం కొనసాగించండి.' : 'Good job! Keep practicing to master this concept.'),
              textAlign: TextAlign.center,
            ),
            if (isStruggling) ...[
              const SizedBox(height: 14),
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: AppColors.lightYellow,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Column(
                  children: [
                    const Text('💡 Personalized Practice Available',
                        style: TextStyle(fontWeight: FontWeight.bold, color: AppColors.textDark)),
                    const SizedBox(height: 4),
                    const Text('Would you like simpler analogies and targeted exercises with Bala Buddy?'),
                    const SizedBox(height: 8),
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.coralOrange,
                        foregroundColor: Colors.white,
                      ),
                      onPressed: () {
                        Navigator.of(context).pop();
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) => const PersonalizedPracticeScreen(
                              topicId: 'bio_ch1_t1',
                              topicTitle: 'Photosynthesis',
                            ),
                          ),
                        );
                      },
                      child: const Text('Start Personalized Practice 💡'),
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              Navigator.of(context).pop(); // Back to topic
            },
            child: const Text('OK', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }
}

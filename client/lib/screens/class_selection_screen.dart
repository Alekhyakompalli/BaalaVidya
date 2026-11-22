import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/models/curriculum_models.dart';
import 'package:baalavidya/models/mock_data.dart';
import 'package:baalavidya/screens/chapter_view_screen.dart';
import 'package:baalavidya/screens/story_mode_screen.dart';
import 'package:baalavidya/screens/subject_view_screen.dart';
import 'package:baalavidya/screens/topic_view_screen.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';
import 'package:baalavidya/widgets/language_toggle.dart';
import 'package:baalavidya/widgets/subject_card.dart';

/// Class Selection screen with Medium Tabs (English Medium & Telugu Medium)
/// and chapter-wise syllabus visibility.
class ClassSelectionScreen extends ConsumerStatefulWidget {
  final ClassItem classItem;

  const ClassSelectionScreen({
    super.key,
    required this.classItem,
  });

  @override
  ConsumerState<ClassSelectionScreen> createState() => _ClassSelectionScreenState();
}

class _ClassSelectionScreenState extends ConsumerState<ClassSelectionScreen> {
  String _selectedMedium = 'EM'; // 'EM' for English Medium, 'TM' for Telugu Medium
  final Set<String> _expandedSubjectIds = {};

  void _toggleSubjectChapters(String subjectId) {
    setState(() {
      if (_expandedSubjectIds.contains(subjectId)) {
        _expandedSubjectIds.remove(subjectId);
      } else {
        _expandedSubjectIds.add(subjectId);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);
    final subjects = MockCurriculumData.getSubjectsForMedium(widget.classItem.id, _selectedMedium);

    final totalChapters = subjects.fold<int>(0, (sum, s) => sum + s.chapterCount);

    return Scaffold(
      backgroundColor: AppColors.softBackground,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        title: Text(
          widget.classItem.localizedName(lang),
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: AppColors.textDark,
          ),
        ),
        actions: const [
          LanguageToggle(),
          SizedBox(width: 8),
        ],
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Syllabus Overview Banner
              Container(
                padding: const EdgeInsets.all(16.0),
                decoration: BoxDecoration(
                  color: AppColors.lightBlue,
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: AppColors.primaryBlue.withOpacity(0.3), width: 1.5),
                ),
                child: Row(
                  children: [
                    const Text('📋', style: TextStyle(fontSize: 32)),
                    const SizedBox(width: 14),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            lang == 'te'
                                ? 'తెలంగాణ SCERT సిలబస్ - ${widget.classItem.localizedName(lang)}'
                                : 'Telangana SCERT - ${widget.classItem.localizedName(lang)}',
                            style: const TextStyle(
                              fontSize: 17,
                              fontWeight: FontWeight.bold,
                              color: AppColors.darkBlue,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            lang == 'te'
                                ? '${_selectedMedium == 'EM' ? 'ఆంగ్ల మాధ్యమం' : 'తెలుగు మాధ్యమం'} • ${subjects.length} సబ్జెక్టులు • $totalChapters అధ్యాయాలు'
                                : '${_selectedMedium == 'EM' ? 'English Medium' : 'Telugu Medium'} • ${subjects.length} Subjects Available • $totalChapters Chapters',
                            style: const TextStyle(
                              fontSize: 14,
                              color: AppColors.textMuted,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 16),

              // Medium Selection Tabs
              Container(
                padding: const EdgeInsets.all(4),
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
                child: Row(
                  children: [
                    // English Medium Tab
                    Expanded(
                      child: InkWell(
                        borderRadius: BorderRadius.circular(12),
                        onTap: () {
                          if (_selectedMedium != 'EM') {
                            setState(() {
                              _selectedMedium = 'EM';
                              _expandedSubjectIds.clear();
                            });
                          }
                        },
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 200),
                          padding: const EdgeInsets.symmetric(vertical: 12),
                          decoration: BoxDecoration(
                            color: _selectedMedium == 'EM' ? AppColors.primaryBlue : Colors.transparent,
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Text('🇬🇧 ', style: TextStyle(fontSize: 18)),
                              Text(
                                lang == 'te' ? 'ఆంగ్ల మాధ్యమం' : 'English Medium',
                                style: TextStyle(
                                  fontSize: 15,
                                  fontWeight: FontWeight.bold,
                                  color: _selectedMedium == 'EM' ? Colors.white : AppColors.textDark,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 4),
                    // Telugu Medium Tab
                    Expanded(
                      child: InkWell(
                        borderRadius: BorderRadius.circular(12),
                        onTap: () {
                          if (_selectedMedium != 'TM') {
                            setState(() {
                              _selectedMedium = 'TM';
                              _expandedSubjectIds.clear();
                            });
                          }
                        },
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 200),
                          padding: const EdgeInsets.symmetric(vertical: 12),
                          decoration: BoxDecoration(
                            color: _selectedMedium == 'TM' ? AppColors.coralOrange : Colors.transparent,
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Text('🇮🇳 ', style: TextStyle(fontSize: 18)),
                              Text(
                                lang == 'te' ? 'తెలుగు మాధ్యమం' : 'Telugu Medium',
                                style: TextStyle(
                                  fontSize: 15,
                                  fontWeight: FontWeight.bold,
                                  color: _selectedMedium == 'TM' ? Colors.white : AppColors.textDark,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 16),

              // Phase 8: Story Mode banner (for lower classes)
              if (int.tryParse(widget.classItem.id) != null && int.parse(widget.classItem.id) <= 5) ...[
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(16.0),
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [Color(0xFFE8F5E9), Color(0xFFC8E6C9)],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: AppColors.meadowGreen, width: 1.5),
                  ),
                  child: Row(
                    children: [
                      const Text('🐰', style: TextStyle(fontSize: 34)),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              lang == 'te' ? 'కథల రూపంలో చదువు (తరగతులు 1-5)' : 'Story Mode: Bala Rabbit (Classes 1-5)',
                              style: const TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: AppColors.darkGreen,
                              ),
                            ),
                            const SizedBox(height: 2),
                            Text(
                              lang == 'te'
                                  ? 'బాల కుందేలుతో సరదా కథల ద్వారా గణిత భావనలను నేర్చుకోండి!'
                                  : 'Explore interactive cartoon narratives & division adventures!',
                              style: const TextStyle(fontSize: 12, color: AppColors.textDark),
                            ),
                          ],
                        ),
                      ),
                      ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.meadowGreen,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                        ),
                        onPressed: () {
                          Navigator.of(context).push(
                            MaterialPageRoute(builder: (context) => const StoryModeScreen()),
                          );
                        },
                        child: Text(
                          lang == 'te' ? 'ప్రారంభించు' : 'Play',
                          style: const TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),
              ],

              // Section Header: Available Subjects & Chapter Syllabus
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      const Text('📚', style: TextStyle(fontSize: 22)),
                      const SizedBox(width: 8),
                      Text(
                        lang == 'te'
                            ? '${_selectedMedium == 'EM' ? 'ఆంగ్ల మాధ్యమ' : 'తెలుగు మాధ్యమ'} సబ్జెక్టులు:'
                            : '${_selectedMedium == 'EM' ? 'English Medium' : 'Telugu Medium'} Subjects:',
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: AppColors.textDark,
                        ),
                      ),
                    ],
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: _selectedMedium == 'EM' ? AppColors.lightBlue : AppColors.lightOrange,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Text(
                      '${subjects.length} ${lang == 'te' ? 'సబ్జెక్టులు' : 'Subjects'}',
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                        color: _selectedMedium == 'EM' ? AppColors.primaryBlue : AppColors.coralOrange,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),

              // Subjects List with Chapter-wise Syllabus Visible
              ListView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: subjects.length,
                itemBuilder: (context, index) {
                  final subject = subjects[index];
                  final chapters = MockCurriculumData.getChaptersForSubject(subject.id);
                  final isExpanded = _expandedSubjectIds.contains(subject.id);

                  return Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Subject Card
                      SubjectCard(
                        subject: subject,
                        onTap: () {
                          ref.read(selectedSubjectProvider.notifier).state = subject;
                          Navigator.of(context).push(
                            MaterialPageRoute(
                              builder: (context) => SubjectViewScreen(subject: subject),
                            ),
                          );
                        },
                      ),

                      // Chapter-wise Syllabus Toggle Bar
                      Container(
                        margin: const EdgeInsets.only(left: 8, right: 8, bottom: 8, top: 0),
                        child: Material(
                          color: Colors.transparent,
                          child: InkWell(
                            borderRadius: BorderRadius.circular(12),
                            onTap: () => _toggleSubjectChapters(subject.id),
                            child: Container(
                              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                              decoration: BoxDecoration(
                                color: subject.lightColor.withOpacity(0.5),
                                borderRadius: BorderRadius.circular(12),
                                border: Border.all(color: subject.color.withOpacity(0.3)),
                              ),
                              child: Row(
                                children: [
                                  Icon(
                                    isExpanded ? Icons.menu_book : Icons.list_alt_rounded,
                                    size: 18,
                                    color: subject.color,
                                  ),
                                  const SizedBox(width: 8),
                                  Expanded(
                                    child: Text(
                                      isExpanded
                                          ? (lang == 'te' ? 'అధ్యాయాల సిలబస్ దాచు' : 'Hide Chapter Syllabus')
                                          : (lang == 'te'
                                              ? 'అధ్యాయాల వారీగా సిలబస్ చూడండి (${chapters.length} అధ్యాయాలు)'
                                              : 'View Chapter-wise Syllabus (${chapters.length} Chapters)'),
                                      style: TextStyle(
                                        fontSize: 13,
                                        fontWeight: FontWeight.w700,
                                        color: subject.color,
                                      ),
                                    ),
                                  ),
                                  Icon(
                                    isExpanded ? Icons.expand_less_rounded : Icons.expand_more_rounded,
                                    color: subject.color,
                                  ),
                                ],
                              ),
                            ),
                          ),
                        ),
                      ),

                      // Chapter-wise Syllabus Expanded View
                      if (isExpanded)
                        Container(
                          margin: const EdgeInsets.only(left: 8, right: 8, bottom: 16),
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(color: subject.color.withOpacity(0.25), width: 1.5),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.black.withOpacity(0.03),
                                blurRadius: 4,
                                offset: const Offset(0, 2),
                              ),
                            ],
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Padding(
                                padding: const EdgeInsets.only(bottom: 8.0),
                                child: Text(
                                  lang == 'te'
                                      ? '${subject.localizedName(lang)} - అధ్యాయాల జాబితా:'
                                      : '${subject.localizedName(lang)} - Chapter-wise Syllabus:',
                                  style: TextStyle(
                                    fontSize: 14,
                                    fontWeight: FontWeight.bold,
                                    color: subject.color,
                                  ),
                                ),
                              ),
                              const Divider(height: 1),
                              ...chapters.map((ch) {
                                return Container(
                                  padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 4.0),
                                  decoration: const BoxDecoration(
                                    border: Border(bottom: BorderSide(color: Color(0xFFF0F0F0))),
                                  ),
                                  child: Row(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Container(
                                        width: 28,
                                        height: 28,
                                        decoration: BoxDecoration(
                                          color: subject.lightColor,
                                          borderRadius: BorderRadius.circular(8),
                                        ),
                                        alignment: Alignment.center,
                                        child: Text(
                                          '${ch.number}',
                                          style: TextStyle(
                                            fontSize: 13,
                                            fontWeight: FontWeight.bold,
                                            color: subject.color,
                                          ),
                                        ),
                                      ),
                                      const SizedBox(width: 10),
                                      Expanded(
                                        child: Column(
                                          crossAxisAlignment: CrossAxisAlignment.start,
                                          children: [
                                            Text(
                                              ch.localizedTitle(lang),
                                              style: const TextStyle(
                                                fontSize: 14,
                                                fontWeight: FontWeight.w600,
                                                color: AppColors.textDark,
                                              ),
                                            ),
                                            const SizedBox(height: 2),
                                            Text(
                                              '${ch.topics.length} ${lang == 'te' ? 'అంశాలు' : 'Topics'}: ${ch.topics.map((t) => t.localizedTitle(lang)).take(3).join(', ')}${ch.topics.length > 3 ? '...' : ''}',
                                              style: const TextStyle(
                                                fontSize: 12,
                                                color: AppColors.textMuted,
                                              ),
                                            ),
                                          ],
                                        ),
                                      ),
                                      InkWell(
                                        borderRadius: BorderRadius.circular(10),
                                        onTap: () {
                                          ref.read(selectedSubjectProvider.notifier).state = subject;
                                          Navigator.of(context).push(
                                            MaterialPageRoute(
                                              builder: (context) => ChapterViewScreen(
                                                chapter: ch,
                                                subject: subject,
                                              ),
                                            ),
                                          );
                                        },
                                        child: Container(
                                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                                          decoration: BoxDecoration(
                                            color: subject.lightColor,
                                            borderRadius: BorderRadius.circular(10),
                                          ),
                                          child: Text(
                                            lang == 'te' ? 'అంశాలు & వీడియో ➔' : 'View Topics & Video ➔',
                                            style: TextStyle(
                                              fontSize: 12,
                                              fontWeight: FontWeight.bold,
                                              color: subject.color,
                                            ),
                                          ),
                                        ),
                                      ),
                                    ],
                                  ),
                                );
                              }),
                              const SizedBox(height: 8),
                              SizedBox(
                                width: double.infinity,
                                child: ElevatedButton.icon(
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: subject.color,
                                    foregroundColor: Colors.white,
                                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                                    padding: const EdgeInsets.symmetric(vertical: 8),
                                  ),
                                  icon: const Icon(Icons.menu_book, size: 16),
                                  label: Text(
                                    lang == 'te'
                                        ? 'పూర్తి సబ్జెక్ట్ అధ్యాయాల ప్రయాణాన్ని తెరవండి'
                                        : 'Open Full Subject Journey ➔',
                                    style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold),
                                  ),
                                  onPressed: () {
                                    ref.read(selectedSubjectProvider.notifier).state = subject;
                                    Navigator.of(context).push(
                                      MaterialPageRoute(
                                        builder: (context) => SubjectViewScreen(subject: subject),
                                      ),
                                    );
                                  },
                                ),
                              ),
                            ],
                          ),
                        ),
                    ],
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}

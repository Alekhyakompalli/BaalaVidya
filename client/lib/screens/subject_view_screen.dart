import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/models/curriculum_models.dart';
import 'package:baalavidya/models/mock_data.dart';
import 'package:baalavidya/screens/mission_challenge_screen.dart';
import 'package:baalavidya/screens/topic_view_screen.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';
import 'package:baalavidya/widgets/chapter_card.dart';
import 'package:baalavidya/widgets/language_toggle.dart';

/// Subject View screen adhering to [PS: 4. Subject View].
/// Features:
/// - Subject name and syllabus progress percentage.
/// - Chapters, lessons, and topics list.
/// - Tapping a topic navigates to TopicViewScreen (Tap 3).
class SubjectViewScreen extends ConsumerWidget {
  final SubjectItem subject;

  const SubjectViewScreen({
    super.key,
    required this.subject,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(languageProvider);
    final chapters = MockCurriculumData.getChaptersForSubject(subject.id);

    return Scaffold(
      backgroundColor: AppColors.softBackground,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        title: Text(
          subject.localizedName(lang),
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
              // Progress Overview Card
              Container(
                padding: const EdgeInsets.all(16.0),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: subject.color.withOpacity(0.3), width: 1.5),
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
                    Row(
                      children: [
                        Text(subject.iconEmoji, style: const TextStyle(fontSize: 28)),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Text(
                            lang == 'te' ? 'మీ అభ్యాస పురోగతి:' : 'Your Learning Progress:',
                            style: const TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: AppColors.textDark,
                            ),
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            color: subject.lightColor,
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Text(
                            '${subject.progressPercentage}%',
                            style: TextStyle(
                              fontSize: 14,
                              fontWeight: FontWeight.bold,
                              color: subject.color,
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    ClipRRect(
                      borderRadius: BorderRadius.circular(8),
                      child: LinearProgressIndicator(
                        value: subject.progressPercentage / 100.0,
                        minHeight: 10,
                        backgroundColor: AppColors.borderColor,
                        valueColor: AlwaysStoppedAnimation<Color>(subject.color),
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      lang == 'te'
                          ? '2/6 పాఠాలు పూర్తయ్యాయి • బాగా నేర్చుకుంటున్నారు! 🌟'
                          : '2 of 6 lessons completed • Keep it up! 🌟',
                      style: const TextStyle(fontSize: 13, color: AppColors.textMuted),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              // Lessons Header
              Row(
                children: [
                  const Text('📖', style: TextStyle(fontSize: 22)),
                  const SizedBox(width: 8),
                  Text(
                    lang == 'te' ? 'పాఠాలు & అంశాలు:' : 'Lessons & Topics:',
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: AppColors.textDark,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),

              // Chapter Cards List
              ListView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: chapters.length,
                itemBuilder: (context, index) {
                  final chapter = chapters[index];
                  return ChapterCard(
                    chapter: chapter,
                    onTopicTap: (topic) {
                      ref.read(selectedTopicProvider.notifier).state = topic;
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (context) => TopicViewScreen(topic: topic),
                        ),
                      );
                    },
                  );
                },
              ),
              const SizedBox(height: 18),

              // Phase 8: End-of-Chapter Mission Challenge [PS: 11. End-of-Chapter Challenge]
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(18.0),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFFFFF3E0), Color(0xFFFFE0B2)],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(22),
                  border: Border.all(color: AppColors.coralOrange, width: 2),
                  boxShadow: [
                    BoxShadow(
                      color: AppColors.coralOrange.withOpacity(0.15),
                      blurRadius: 10,
                      offset: const Offset(0, 3),
                    ),
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Text('🏅', style: TextStyle(fontSize: 32)),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                lang == 'te' ? 'అధ్యాయం మిషన్ ఛాలెంజ్' : 'Chapter Mission Challenge',
                                style: const TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                  color: Color(0xFFE65100),
                                ),
                              ),
                              const SizedBox(height: 2),
                              Text(
                                lang == 'te'
                                    ? 'క్విజ్, పజిల్స్ & సవాళ్ళతో చాప్టర్ బ్యాడ్జ్ మరియు సర్టిఫికేట్ గెలవండి!'
                                    : 'Quiz, puzzle & scenario to earn your Chapter Badge & Certificate!',
                                style: const TextStyle(fontSize: 13, color: AppColors.textDark),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 14),
                    ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.coralOrange,
                        foregroundColor: Colors.white,
                        minimumSize: const Size(double.infinity, 48),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                      ),
                      icon: const Text('🚀', style: TextStyle(fontSize: 18)),
                      label: Text(
                        lang == 'te' ? 'మిషన్ ఛాలెంజ్ ప్రారంభించు (+50 XP)' : 'Start Mission Challenge (+50 XP)',
                        style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                      ),
                      onPressed: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) => const MissionChallengeScreen(chapterId: 'bio_ch1'),
                          ),
                        );
                      },
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 12),
            ],
          ),
        ),
      ),
    );
  }
}

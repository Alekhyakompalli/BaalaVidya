import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/models/curriculum_models.dart';
import 'package:baalavidya/models/mock_data.dart';
import 'package:baalavidya/screens/home_screen.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';
import 'package:baalavidya/widgets/language_toggle.dart';

/// Login Screen asking for Student Name, Class, and Medium.
/// Displayed first upon opening the app.
class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController(text: 'Alekhya');
  String _selectedClassId = '6';
  String _selectedMedium = 'EM'; // 'EM' or 'TM'

  final List<ClassItem> _availableClasses = MockCurriculumData.classes;

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }

  void _onStartLearning() {
    if (!_formKey.currentState!.validate()) return;

    final studentName = _nameController.text.trim();
    ref.read(currentLearnerNameProvider.notifier).state = studentName;

    final classItem = _availableClasses.firstWhere(
      (c) => c.id == _selectedClassId,
      orElse: () => _availableClasses.first,
    );
    ref.read(selectedClassProvider.notifier).state = classItem;

    // Set app language based on chosen medium
    final lang = _selectedMedium == 'TM' ? 'te' : 'en';
    ref.read(languageProvider.notifier).state = lang;

    // Set default subject for the chosen class and medium
    final subjects = MockCurriculumData.getSubjectsForMedium(classItem.id, _selectedMedium);
    if (subjects.isNotEmpty) {
      ref.read(selectedSubjectProvider.notifier).state = subjects.first;
    }

    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (context) => const HomeScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);
    final isTelugu = lang == 'te' || _selectedMedium == 'TM';

    return Scaffold(
      backgroundColor: AppColors.softBackground,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        title: Text(
          isTelugu ? 'విద్యార్థి లాగిన్' : 'Student Login',
          style: const TextStyle(
            fontSize: 18,
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
          padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Mascot & Branding Header
                Center(
                  child: Column(
                    children: [
                      Container(
                        width: 90,
                        height: 90,
                        decoration: BoxDecoration(
                          color: AppColors.primaryBlue,
                          shape: BoxShape.circle,
                          boxShadow: [
                            BoxShadow(
                              color: AppColors.primaryBlue.withOpacity(0.3),
                              blurRadius: 16,
                              offset: const Offset(0, 6),
                            ),
                          ],
                        ),
                        alignment: Alignment.center,
                        child: const Text('🎓', style: TextStyle(fontSize: 48)),
                      ),
                      const SizedBox(height: 14),
                      Text(
                        isTelugu ? 'బాలవిద్య' : 'BAALAVIDYA',
                        style: const TextStyle(
                          fontSize: 26,
                          fontWeight: FontWeight.w900,
                          color: AppColors.primaryBlue,
                          letterSpacing: 1.2,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        isTelugu
                            ? 'మీ వ్యక్తిగతీకరించిన AI అభ్యాస మిత్రుడు 🌟'
                            : 'Your Personalized AI Learning Companion 🌟',
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w600,
                          color: AppColors.textMuted,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 28),

                // Card Container
                Container(
                  padding: const EdgeInsets.all(20.0),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(24),
                    border: Border.all(color: AppColors.borderColor, width: 1.5),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.04),
                        blurRadius: 12,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // 1. Name Field
                      Row(
                        children: [
                          const Text('👤', style: TextStyle(fontSize: 20)),
                          const SizedBox(width: 8),
                          Text(
                            isTelugu ? 'మీ పేరు రాయండి:' : 'Enter Your Name:',
                            style: const TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: AppColors.textDark,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      TextFormField(
                        controller: _nameController,
                        decoration: InputDecoration(
                          hintText: isTelugu ? 'ఉదా: అలేఖ్య / రాజేష్' : 'e.g. Alekhya / Rahul',
                          prefixIcon: const Icon(Icons.badge_rounded, color: AppColors.primaryBlue),
                          filled: true,
                          fillColor: AppColors.softBackground,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(16),
                            borderSide: const BorderSide(color: AppColors.borderColor),
                          ),
                          enabledBorder: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(16),
                            borderSide: const BorderSide(color: AppColors.borderColor),
                          ),
                          focusedBorder: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(16),
                            borderSide: const BorderSide(color: AppColors.primaryBlue, width: 2),
                          ),
                        ),
                        validator: (value) {
                          if (value == null || value.trim().isEmpty) {
                            return isTelugu ? 'దయచేసి మీ పేరును నమోదు చేయండి' : 'Please enter your name';
                          }
                          return null;
                        },
                      ),
                      const SizedBox(height: 22),

                      // 2. Select Medium
                      Row(
                        children: [
                          const Text('🌐', style: TextStyle(fontSize: 20)),
                          const SizedBox(width: 8),
                          Text(
                            isTelugu ? 'మీడియం ఎంచుకోండి:' : 'Select Medium:',
                            style: const TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: AppColors.textDark,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 10),
                      Row(
                        children: [
                          // English Medium Tab
                          Expanded(
                            child: InkWell(
                              borderRadius: BorderRadius.circular(14),
                              onTap: () {
                                setState(() {
                                  _selectedMedium = 'EM';
                                });
                                ref.read(languageProvider.notifier).state = 'en';
                              },
                              child: AnimatedContainer(
                                duration: const Duration(milliseconds: 200),
                                padding: const EdgeInsets.symmetric(vertical: 12),
                                decoration: BoxDecoration(
                                  color: _selectedMedium == 'EM'
                                      ? AppColors.primaryBlue
                                      : AppColors.softBackground,
                                  borderRadius: BorderRadius.circular(14),
                                  border: Border.all(
                                    color: _selectedMedium == 'EM'
                                        ? AppColors.primaryBlue
                                        : AppColors.borderColor,
                                    width: 1.5,
                                  ),
                                ),
                                child: Center(
                                  child: Text(
                                    '🇬🇧 English Medium',
                                    style: TextStyle(
                                      fontSize: 14,
                                      fontWeight: FontWeight.bold,
                                      color: _selectedMedium == 'EM'
                                          ? Colors.white
                                          : AppColors.textDark,
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ),
                          const SizedBox(width: 10),
                          // Telugu Medium Tab
                          Expanded(
                            child: InkWell(
                              borderRadius: BorderRadius.circular(14),
                              onTap: () {
                                setState(() {
                                  _selectedMedium = 'TM';
                                });
                                ref.read(languageProvider.notifier).state = 'te';
                              },
                              child: AnimatedContainer(
                                duration: const Duration(milliseconds: 200),
                                padding: const EdgeInsets.symmetric(vertical: 12),
                                decoration: BoxDecoration(
                                  color: _selectedMedium == 'TM'
                                      ? AppColors.coralOrange
                                      : AppColors.softBackground,
                                  borderRadius: BorderRadius.circular(14),
                                  border: Border.all(
                                    color: _selectedMedium == 'TM'
                                        ? AppColors.coralOrange
                                        : AppColors.borderColor,
                                    width: 1.5,
                                  ),
                                ),
                                child: Center(
                                  child: Text(
                                    '🇮🇳 తెలుగు మీడియం',
                                    style: TextStyle(
                                      fontSize: 14,
                                      fontWeight: FontWeight.bold,
                                      color: _selectedMedium == 'TM'
                                          ? Colors.white
                                          : AppColors.textDark,
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 22),

                      // 3. Select Class
                      Row(
                        children: [
                          const Text('🏫', style: TextStyle(fontSize: 20)),
                          const SizedBox(width: 8),
                          Text(
                            isTelugu ? 'మీ తరగతిని ఎంచుకోండి:' : 'Select Your Class:',
                            style: const TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: AppColors.textDark,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 10),
                      GridView.builder(
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                          crossAxisCount: 5,
                          crossAxisSpacing: 8,
                          mainAxisSpacing: 8,
                          childAspectRatio: 0.9,
                        ),
                        itemCount: _availableClasses.length,
                        itemBuilder: (context, index) {
                          final c = _availableClasses[index];
                          final isSelected = c.id == _selectedClassId;

                          return InkWell(
                            borderRadius: BorderRadius.circular(16),
                            onTap: () {
                              setState(() {
                                _selectedClassId = c.id;
                              });
                            },
                            child: AnimatedContainer(
                              duration: const Duration(milliseconds: 200),
                              decoration: BoxDecoration(
                                color: isSelected ? c.color : c.lightColor.withOpacity(0.5),
                                borderRadius: BorderRadius.circular(16),
                                border: Border.all(
                                  color: isSelected ? c.color : AppColors.borderColor,
                                  width: isSelected ? 2.5 : 1,
                                ),
                                boxShadow: isSelected
                                    ? [
                                        BoxShadow(
                                          color: c.color.withOpacity(0.4),
                                          blurRadius: 8,
                                          offset: const Offset(0, 3),
                                        ),
                                      ]
                                    : [],
                              ),
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Text(c.iconEmoji, style: const TextStyle(fontSize: 22)),
                                  const SizedBox(height: 4),
                                  Text(
                                    isTelugu ? '${c.id}వ' : 'Cl ${c.id}',
                                    style: TextStyle(
                                      fontSize: 14,
                                      fontWeight: FontWeight.bold,
                                      color: isSelected ? Colors.white : AppColors.textDark,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 28),

                // Start Learning CTA Button
                ElevatedButton(
                  onPressed: _onStartLearning,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primaryBlue,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(18),
                    ),
                    elevation: 3,
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        isTelugu ? 'నేర్చుకోవడం ప్రారంభిద్దాం! 🚀' : 'Start Learning! 🚀',
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          letterSpacing: 0.5,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

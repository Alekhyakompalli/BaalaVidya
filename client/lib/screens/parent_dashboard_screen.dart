import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/l10n/app_strings.dart';
import 'package:baalavidya/models/analytics_models.dart';
import 'package:baalavidya/services/analytics_service.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';
import 'package:baalavidya/widgets/language_toggle.dart';
import 'package:baalavidya/widgets/offline_banner.dart';

/// Parent Dashboard & Analytics Screen [PS: 10. Parent Dashboard; Parent Insights].
/// Adheres to:
/// - [Arch: Parent visibility; Child privacy]
/// - [R11: Parental Gate & Consent]
/// - [ADR 0011: Parent Dashboard, Analytics & Child Privacy Architecture]
/// - Strict Child Privacy: Zero chat transcripts exposed.
/// - Minimum Data Notice for early learner sessions.
class ParentDashboardScreen extends ConsumerStatefulWidget {
  final bool initiallyUnlocked;

  const ParentDashboardScreen({
    super.key,
    this.initiallyUnlocked = false,
  });

  @override
  ConsumerState<ParentDashboardScreen> createState() => _ParentDashboardScreenState();
}

class _ParentDashboardScreenState extends ConsumerState<ParentDashboardScreen> {
  late bool _isUnlocked;
  final TextEditingController _pinController = TextEditingController();
  String? _pinError;
  bool _isLoading = false;
  ParentDashboardData? _dashboardData;
  final AnalyticsService _analyticsService = AnalyticsService();

  @override
  void initState() {
    super.initState();
    _isUnlocked = widget.initiallyUnlocked;
    if (_isUnlocked) {
      _loadDashboardData();
    }
  }

  @override
  void dispose() {
    _pinController.dispose();
    super.dispose();
  }

  Future<void> _verifyPin() async {
    final pin = _pinController.text.trim();
    final learnerId = ref.read(currentLearnerIdProvider);
    final lang = ref.read(languageProvider);

    if (pin.isEmpty) {
      setState(() => _pinError = AppStrings.get('invalidPinError', lang));
      return;
    }

    setState(() => _isLoading = true);
    final isValid = await _analyticsService.verifyParentPin(learnerId, pin);

    if (!mounted) return;

    if (isValid) {
      setState(() {
        _isUnlocked = true;
        _pinError = null;
        _isLoading = false;
      });
      _loadDashboardData();
    } else {
      setState(() {
        _pinError = AppStrings.get('invalidPinError', lang);
        _isLoading = false;
      });
    }
  }

  Future<void> _loadDashboardData() async {
    setState(() => _isLoading = true);

    final learnerId = ref.read(currentLearnerIdProvider);
    final learnerName = ref.read(currentLearnerNameProvider);
    final xp = ref.read(learnerXpProvider);
    final level = ref.read(learnerLevelProvider);
    final levelName = ref.read(learnerLevelNameProvider);
    final streak = ref.read(learnerStreakProvider);
    final coins = ref.read(learnerCoinsProvider);
    final stars = ref.read(learnerStarsProvider);
    final badges = ref.read(learnerBadgesProvider);
    final completedTopics = ref.read(completedTopicsProvider);
    final qCount = ref.read(questionsAskedProvider);

    final data = await _analyticsService.getParentAnalytics(
      learnerId: learnerId,
      learnerName: learnerName,
      xp: xp,
      level: level,
      levelName: levelName,
      streak: streak,
      coins: coins,
      stars: stars,
      badges: badges,
      completedTopics: completedTopics,
      questionsAsked: qCount,
    );

    if (mounted) {
      setState(() {
        _dashboardData = data;
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);

    return Scaffold(
      backgroundColor: AppColors.softBackground,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        title: Text(
          AppStrings.get('parentDashboardTitle', lang),
          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppColors.textDark),
        ),
        actions: [
          const LanguageToggle(),
          if (_isUnlocked)
            IconButton(
              icon: const Icon(Icons.lock_outline, color: AppColors.textMuted),
              tooltip: AppStrings.get('exitParentZone', lang),
              onPressed: () {
                setState(() {
                  _isUnlocked = false;
                  _pinController.clear();
                });
              },
            ),
          const SizedBox(width: 8),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            const OfflineBanner(),
            Expanded(
              child: _isLoading && _dashboardData == null
                  ? const Center(child: CircularProgressIndicator())
                  : !_isUnlocked
                      ? _buildParentalGate(lang)
                      : _buildDashboardContent(lang),
            ),
          ],
        ),
      ),
    );
  }

  /// Parental Gate View (R11)
  Widget _buildParentalGate(String lang) {
    return Center(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Card(
          elevation: 3,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: AppColors.primary.withOpacity(0.1),
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(Icons.lock_rounded, size: 48, color: AppColors.primary),
                ),
                const SizedBox(height: 16),
                Text(
                  AppStrings.get('parentalGateTitle', lang),
                  style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: AppColors.textDark),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  AppStrings.get('parentalGatePrompt', lang),
                  style: const TextStyle(fontSize: 14, color: AppColors.textMuted),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 20),
                SizedBox(
                  width: 180,
                  child: TextField(
                    controller: _pinController,
                    keyboardType: TextInputType.number,
                    obscureText: true,
                    maxLength: 4,
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, letterSpacing: 8),
                    decoration: InputDecoration(
                      counterText: '',
                      hintText: '••••',
                      errorText: _pinError,
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                      contentPadding: const EdgeInsets.symmetric(vertical: 12),
                    ),
                    onSubmitted: (_) => _verifyPin(),
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  AppStrings.get('parentalGateDefaultHint', lang),
                  style: const TextStyle(fontSize: 12, color: AppColors.textMuted, fontStyle: FontStyle.italic),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 20),
                SizedBox(
                  width: double.infinity,
                  height: 48,
                  child: ElevatedButton(
                    onPressed: _isLoading ? null : _verifyPin,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primary,
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                    child: _isLoading
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                          )
                        : Text(
                            AppStrings.get('unlockParentZone', lang),
                            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                          ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  /// Full Parent Dashboard Content
  Widget _buildDashboardContent(String lang) {
    final data = _dashboardData;
    if (data == null) {
      return const Center(child: CircularProgressIndicator());
    }

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // 1. Learner Profile Header
          _buildLearnerHeader(data, lang),
          const SizedBox(height: 16),

          // 2. Child Privacy Protected Assurance Card [Arch: Parent visibility]
          _buildPrivacyNoticeCard(data, lang),
          const SizedBox(height: 16),

          // 3. Minimum Data Notice Banner (if applicable)
          if (data.minimumDataNotice != null) ...[
            _buildMinimumDataBanner(data.minimumDataNotice!, lang),
            const SizedBox(height: 16),
          ],

          // 4. Learning Metrics Grid (Time, Streak, XP, Level, Rate)
          _buildMetricsGrid(data, lang),
          const SizedBox(height: 20),

          // 5. Subject Progress Overview
          _buildSubjectProgressSection(data, lang),
          const SizedBox(height: 20),

          // 6. Weak Concepts & Focus Areas
          if (data.weakConcepts.isNotEmpty) ...[
            _buildWeakConceptsSection(data, lang),
            const SizedBox(height: 20),
          ],

          // 7. Strength Areas & Celebrations
          if (data.strengthAreas.isNotEmpty) ...[
            _buildStrengthAreasSection(data, lang),
            const SizedBox(height: 20),
          ],

          // 8. Actionable Recommendations for Parents
          _buildRecommendationsSection(data, lang),
          const SizedBox(height: 24),

          // 8b. Data Management & Privacy [Right to be Forgotten - ADR 0012]
          _buildDataManagementSection(data, lang),
          const SizedBox(height: 24),

          // 9. Return to Student Mode Button
          Center(
            child: TextButton.icon(
              onPressed: () => Navigator.of(context).pop(),
              icon: const Icon(Icons.arrow_back),
              label: Text(AppStrings.get('exitParentZone', lang)),
            ),
          ),
          const SizedBox(height: 16),
        ],
      ),
    );
  }

  Widget _buildLearnerHeader(ParentDashboardData data, String lang) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFF2C3E50), Color(0xFF3498DB)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.08),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Row(
        children: [
          CircleAvatar(
            radius: 28,
            backgroundColor: Colors.white.withOpacity(0.2),
            child: const Text('🎓', style: TextStyle(fontSize: 28)),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '${data.learnerName}\'s Learning Journey',
                  style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
                ),
                const SizedBox(height: 4),
                Text(
                  'Level ${data.currentLevel} • ${data.levelName}',
                  style: TextStyle(fontSize: 13, color: Colors.white.withOpacity(0.9)),
                ),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.2),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text('🔥 ', style: TextStyle(fontSize: 14)),
                Text(
                  '${data.learningStreakDays} ${AppStrings.get('daysCount', lang)}',
                  style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.white),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPrivacyNoticeCard(ParentDashboardData data, String lang) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: const Color(0xFFE8F8F5),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFA3E4D7)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.shield_rounded, color: Color(0xFF16A085), size: 24),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  AppStrings.get('childPrivacyNoticeTitle', lang),
                  style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Color(0xFF0E6655)),
                ),
                const SizedBox(height: 4),
                Text(
                  data.privacyNotice,
                  style: const TextStyle(fontSize: 12, color: Color(0xFF117A65), height: 1.3),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMinimumDataBanner(String notice, String lang) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFFFEF9E7),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFF9E79F)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.info_outline, color: Color(0xFFB7950B), size: 22),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              notice,
              style: const TextStyle(fontSize: 12, color: Color(0xFF7D6608)),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMetricsGrid(ParentDashboardData data, String lang) {
    return Column(
      children: [
        Row(
          children: [
            Expanded(
              child: _buildMetricCard(
                icon: Icons.timer_outlined,
                color: Colors.blue,
                label: AppStrings.get('totalTimeSpent', lang),
                value: '${data.totalTimeSpentMinutes} mins',
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _buildMetricCard(
                icon: Icons.today_outlined,
                color: Colors.teal,
                label: AppStrings.get('timeToday', lang),
                value: '${data.timeSpentTodayMinutes} mins',
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: _buildMetricCard(
                icon: Icons.menu_book_rounded,
                color: Colors.deepPurple,
                label: AppStrings.get('workbookCompletion', lang),
                value: '${data.workbookCompletionRate.toInt()}%',
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _buildMetricCard(
                icon: Icons.sports_esports_rounded,
                color: Colors.orange,
                label: AppStrings.get('gamePerformance', lang),
                value: '${data.gamePerformanceScore.toInt()}%',
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: _buildMetricCard(
                icon: Icons.bolt_rounded,
                color: Colors.amber.shade800,
                label: AppStrings.get('totalXp', lang),
                value: '${data.totalXp} XP',
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _buildMetricCard(
                icon: Icons.star_rounded,
                color: Colors.amber,
                label: AppStrings.get('starsLabel', lang),
                value: '${data.starsEarned} ⭐',
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildMetricCard({
    required IconData icon,
    required Color color,
    required String label,
    required String value,
  }) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.shade200),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: color.withOpacity(0.12),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(icon, color: color, size: 22),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: const TextStyle(fontSize: 11, color: AppColors.textMuted),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 2),
                Text(
                  value,
                  style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: AppColors.textDark),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSubjectProgressSection(ParentDashboardData data, String lang) {
    return Card(
      elevation: 1,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.school_rounded, color: AppColors.primary, size: 20),
                const SizedBox(width: 8),
                Text(
                  AppStrings.get('learningProgress', lang),
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppColors.textDark),
                ),
              ],
            ),
            const SizedBox(height: 14),
            ...data.subjectSummaries.map((sub) {
              final subTitle = lang == 'te' ? sub.teluguSubjectName : sub.subjectName;
              final fraction = (sub.completionPercentage / 100.0).clamp(0.0, 1.0);

              return Padding(
                padding: const EdgeInsets.only(bottom: 12.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          subTitle,
                          style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: AppColors.textDark),
                        ),
                        Text(
                          '${sub.completedTopicsCount}/${sub.totalTopicsCount} topics (${sub.completionPercentage}%)',
                          style: const TextStyle(fontSize: 12, color: AppColors.textMuted),
                        ),
                      ],
                    ),
                    const SizedBox(height: 6),
                    ClipRRect(
                      borderRadius: BorderRadius.circular(6),
                      child: LinearProgressIndicator(
                        value: fraction,
                        minHeight: 8,
                        backgroundColor: Colors.grey.shade200,
                        valueColor: AlwaysStoppedAnimation<Color>(
                          sub.completionPercentage >= 80 ? Colors.green : AppColors.primary,
                        ),
                      ),
                    ),
                  ],
                ),
              );
            }),
          ],
        ),
      ),
    );
  }

  Widget _buildWeakConceptsSection(ParentDashboardData data, String lang) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Icon(Icons.priority_high_rounded, color: Colors.amber, size: 20),
            const SizedBox(width: 8),
            Text(
              AppStrings.get('weakConceptsTitle', lang),
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppColors.textDark),
            ),
          ],
        ),
        const SizedBox(height: 10),
        ...data.weakConcepts.map((c) {
          final title = lang == 'te' ? c.teluguTopicTitle : c.topicTitle;
          final rec = lang == 'te' ? c.teluguRecommendedAction : c.recommendedAction;

          return Container(
            margin: const EdgeInsets.only(bottom: 10),
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.orange.shade200),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Text(
                        title,
                        style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AppColors.textDark),
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: Colors.orange.shade50,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        '${c.accuracyPercentage}% Accuracy',
                        style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.orange.shade800),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.lightbulb_outline, size: 16, color: Colors.orange),
                    const SizedBox(width: 6),
                    Expanded(
                      child: Text(
                        rec,
                        style: const TextStyle(fontSize: 12, color: AppColors.textMuted, height: 1.3),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          );
        }),
      ],
    );
  }

  Widget _buildStrengthAreasSection(ParentDashboardData data, String lang) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Icon(Icons.verified_rounded, color: Colors.green, size: 20),
            const SizedBox(width: 8),
            Text(
              AppStrings.get('strengthsTitle', lang),
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppColors.textDark),
            ),
          ],
        ),
        const SizedBox(height: 10),
        ...data.strengthAreas.map((c) {
          final title = lang == 'te' ? c.teluguTopicTitle : c.topicTitle;
          final rec = lang == 'te' ? c.teluguRecommendedAction : c.recommendedAction;

          return Container(
            margin: const EdgeInsets.only(bottom: 10),
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.green.shade200),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Text(
                        title,
                        style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AppColors.textDark),
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: Colors.green.shade50,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        '${c.accuracyPercentage}% Accuracy',
                        style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.green.shade800),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.thumb_up_alt_outlined, size: 16, color: Colors.green),
                    const SizedBox(width: 6),
                    Expanded(
                      child: Text(
                        rec,
                        style: const TextStyle(fontSize: 12, color: AppColors.textMuted, height: 1.3),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          );
        }),
      ],
    );
  }

  Widget _buildRecommendationsSection(ParentDashboardData data, String lang) {
    final recs = lang == 'te' ? data.teluguImprovementRecommendations : data.improvementRecommendations;

    return Card(
      elevation: 1,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.tips_and_updates_rounded, color: Colors.amber, size: 20),
                const SizedBox(width: 8),
                Text(
                  AppStrings.get('recommendationsTitle', lang),
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppColors.textDark),
                ),
              ],
            ),
            const SizedBox(height: 12),
            ...recs.map((rec) => Padding(
                  padding: const EdgeInsets.only(bottom: 8.0),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('• ', style: TextStyle(fontSize: 16, color: AppColors.primary, fontWeight: FontWeight.bold)),
                      Expanded(
                        child: Text(
                          rec,
                          style: const TextStyle(fontSize: 13, color: AppColors.textDark, height: 1.3),
                        ),
                      ),
                    ],
                  ),
                )),
          ],
        ),
      ),
    );
  }

  Widget _buildDataManagementSection(ParentDashboardData data, String lang) {
    return Card(
      elevation: 1,
      color: Colors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
        side: BorderSide(color: Colors.red.shade100),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.privacy_tip_outlined, color: Colors.redAccent, size: 20),
                const SizedBox(width: 8),
                Text(
                  AppStrings.get('deleteDataTitle', lang),
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppColors.textDark),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              AppStrings.get('deleteDataSubtitle', lang),
              style: const TextStyle(fontSize: 12, color: AppColors.textMuted, height: 1.3),
            ),
            const SizedBox(height: 14),
            SizedBox(
              height: 42,
              child: OutlinedButton.icon(
                onPressed: () => _showDeleteConfirmationDialog(data, lang),
                icon: const Icon(Icons.delete_forever, color: Colors.red),
                label: Text(
                  AppStrings.get('deleteDataButton', lang),
                  style: const TextStyle(color: Colors.red, fontWeight: FontWeight.bold),
                ),
                style: OutlinedButton.styleFrom(
                  side: const BorderSide(color: Colors.redAccent),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showDeleteConfirmationDialog(ParentDashboardData data, String lang) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(AppStrings.get('deleteDataConfirmTitle', lang)),
        content: Text(AppStrings.get('deleteDataConfirmMessage', lang)),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: Text(AppStrings.get('deleteDataCancelBtn', lang)),
          ),
          ElevatedButton(
            onPressed: () async {
              Navigator.of(ctx).pop();
              await _analyticsService.purgeStudentAndParentData(data.learnerId);
              if (!mounted) return;
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text(AppStrings.get('deleteDataSuccessToast', lang))),
              );
              setState(() {
                _isUnlocked = false;
                _pinController.clear();
              });
            },
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red, foregroundColor: Colors.white),
            child: Text(AppStrings.get('deleteDataConfirmBtn', lang)),
          ),
        ],
      ),
    );
  }
}

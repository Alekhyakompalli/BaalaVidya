import 'package:flutter/material.dart';
import 'package:baalavidya/l10n/app_strings.dart';
import 'package:baalavidya/theme/app_theme.dart';

/// Feedback dialog for students, teachers, parents, and volunteers during Phase 11 Pilot.
/// Adheres to:
/// - [PS: Success Metrics 1 to 6]
/// - [Plan: Phase 11 Pilot Scope and Exit Criteria]
/// - [ADR 0013: Pilot Evaluation, Success Metrics & Launch Architecture]
class PilotFeedbackDialog extends StatefulWidget {
  final String currentLanguage;
  final Future<bool> Function(Map<String, dynamic> feedbackData)? onSubmit;

  const PilotFeedbackDialog({
    super.key,
    required this.currentLanguage,
    this.onSubmit,
  });

  static Future<void> show(
    BuildContext context, {
    required String currentLanguage,
    Future<bool> Function(Map<String, dynamic> feedbackData)? onSubmit,
  }) {
    return showDialog<void>(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => PilotFeedbackDialog(
        currentLanguage: currentLanguage,
        onSubmit: onSubmit,
      ),
    );
  }

  @override
  State<PilotFeedbackDialog> createState() => _PilotFeedbackDialogState();
}

class _PilotFeedbackDialogState extends State<PilotFeedbackDialog> {
  String _selectedRole = 'student';
  int _rating = 5;
  final TextEditingController _commentController = TextEditingController();
  bool _isSubmitting = false;
  bool _submitted = false;

  @override
  void dispose() {
    _commentController.dispose();
    super.dispose();
  }

  Future<void> _handleSubmit() async {
    final comment = _commentController.text.trim();
    if (comment.length < 3) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please enter at least 3 characters of feedback.'),
          backgroundColor: AppColors.errorRed,
        ),
      );
      return;
    }

    setState(() => _isSubmitting = true);

    final payload = {
      'stakeholder_role': _selectedRole,
      'rating': _rating,
      'comment': comment,
      'language': widget.currentLanguage,
    };

    if (widget.onSubmit != null) {
      await widget.onSubmit!(payload);
    }

    if (mounted) {
      setState(() {
        _isSubmitting = false;
        _submitted = true;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final lang = widget.currentLanguage;

    if (_submitted) {
      return AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: Row(
          children: [
            const Text('🌟', style: TextStyle(fontSize: 26)),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                AppStrings.get('pilotThankYouTitle', lang),
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
            ),
          ],
        ),
        content: Text(
          AppStrings.get('pilotThankYouMessage', lang),
          style: const TextStyle(fontSize: 15, height: 1.4),
        ),
        actions: [
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primaryBlue,
              foregroundColor: Colors.white,
              minimumSize: const Size(120, 48),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
            onPressed: () => Navigator.of(context).pop(),
            child: Text(AppStrings.get('pilotCloseBtn', lang)),
          ),
        ],
      );
    }

    return AlertDialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      title: Row(
        children: [
          const Text('💬', style: TextStyle(fontSize: 26)),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              AppStrings.get('pilotFeedbackTitle', lang),
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
          ),
        ],
      ),
      content: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              AppStrings.get('pilotFeedbackSubtitle', lang),
              style: const TextStyle(fontSize: 13, color: AppColors.textSecondary),
            ),
            const SizedBox(height: 16),

            // Role selection
            Text(
              AppStrings.get('pilotRolePrompt', lang),
              style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                _buildRoleChoiceChip('student', AppStrings.get('pilotRoleStudent', lang)),
                _buildRoleChoiceChip('teacher', AppStrings.get('pilotRoleTeacher', lang)),
                _buildRoleChoiceChip('parent', AppStrings.get('pilotRoleParent', lang)),
                _buildRoleChoiceChip('volunteer', AppStrings.get('pilotRoleVolunteer', lang)),
              ],
            ),
            const SizedBox(height: 16),

            // Rating Stars
            Text(
              AppStrings.get('pilotRatingPrompt', lang),
              style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(5, (index) {
                final starNum = index + 1;
                return IconButton(
                  key: Key('pilot_star_$starNum'),
                  constraints: const BoxConstraints(minWidth: 48, minHeight: 48),
                  icon: Icon(
                    starNum <= _rating ? Icons.star_rounded : Icons.star_outline_rounded,
                    color: AppColors.accentGold,
                    size: 36,
                  ),
                  onPressed: () => setState(() => _rating = starNum),
                );
              }),
            ),
            const SizedBox(height: 12),

            // Comment textfield
            Text(
              AppStrings.get('pilotCommentPrompt', lang),
              style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            TextField(
              key: const Key('pilot_comment_field'),
              controller: _commentController,
              maxLines: 3,
              decoration: InputDecoration(
                hintText: AppStrings.get('pilotCommentPlaceholder', lang),
                hintStyle: const TextStyle(fontSize: 13, color: AppColors.textSecondary),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                filled: true,
                fillColor: AppColors.surfaceLight,
              ),
            ),
          ],
        ),
      ),
      actions: [
        TextButton(
          style: TextButton.styleFrom(
            minimumSize: const Size(80, 48),
          ),
          onPressed: _isSubmitting ? null : () => Navigator.of(context).pop(),
          child: Text(AppStrings.get('deleteDataCancelBtn', lang)),
        ),
        ElevatedButton(
          key: const Key('pilot_submit_btn'),
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.primaryBlue,
            foregroundColor: Colors.white,
            minimumSize: const Size(120, 48),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          ),
          onPressed: _isSubmitting ? null : _handleSubmit,
          child: _isSubmitting
              ? const SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                )
              : Text(AppStrings.get('pilotSubmitBtn', lang)),
        ),
      ],
    );
  }

  Widget _buildRoleChoiceChip(String roleKey, String label) {
    final isSelected = _selectedRole == roleKey;
    return ChoiceChip(
      key: Key('chip_role_$roleKey'),
      label: Text(label),
      selected: isSelected,
      selectedColor: AppColors.primaryBlue.withAlpha(50),
      backgroundColor: AppColors.surfaceLight,
      labelStyle: TextStyle(
        fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
        color: isSelected ? AppColors.primaryBlue : AppColors.darkBlue,
      ),
      onSelected: (val) {
        if (val) setState(() => _selectedRole = roleKey);
      },
    );
  }
}

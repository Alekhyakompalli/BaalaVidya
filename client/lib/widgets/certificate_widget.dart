import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/models/chapter_package_model.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';

/// Achievement Certificate card & dialog [PS: 11. Learning Rewards; Arch: Gamification engine].
class CertificateWidget extends ConsumerWidget {
  final CertificateModel certificate;

  const CertificateWidget({
    super.key,
    required this.certificate,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(languageProvider);

    return Container(
      width: double.infinity,
      margin: const EdgeInsets.symmetric(vertical: 8),
      padding: const EdgeInsets.all(20.0),
      decoration: BoxDecoration(
        color: const Color(0xFFFFFDF5),
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: const Color(0xFFFFD54F), width: 3),
        boxShadow: [
          BoxShadow(
            color: Colors.amber.withOpacity(0.18),
            blurRadius: 14,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        children: [
          // Ribbon & Header
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text('📜', style: TextStyle(fontSize: 32)),
              const SizedBox(width: 8),
              Text(
                lang == 'te' ? 'విజయ ధ్రువీకరణ పత్రం' : 'CERTIFICATE OF EXCELLENCE',
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w900,
                  letterSpacing: 1.2,
                  color: Color(0xFF8D6E63),
                ),
              ),
              const SizedBox(width: 8),
              const Text('⭐', style: TextStyle(fontSize: 28)),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            lang == 'te'
                ? 'తెలంగాణ ఎస్.సి.ఇ.ఆర్.టి సిలబస్ అభ్యాసంలో ప్రతిభ కనబరిచినందుకు'
                : 'This is proudly presented for outstanding learning achievement to',
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 13, color: AppColors.textMuted, fontStyle: FontStyle.italic),
          ),
          const SizedBox(height: 10),

          // Learner Name
          Text(
            certificate.learnerName,
            style: const TextStyle(
              fontSize: 26,
              fontWeight: FontWeight.bold,
              color: AppColors.primaryBlue,
              decoration: TextDecoration.underline,
              decorationColor: AppColors.sunshineYellow,
              decorationThickness: 2,
            ),
          ),
          const SizedBox(height: 10),

          Text(
            lang == 'te'
                ? 'పాఠ్యాంశం విజయవంతంగా పూర్తి చేశారు:'
                : 'for successfully mastering and completing the chapter:',
            style: const TextStyle(fontSize: 13, color: AppColors.textMuted),
          ),
          const SizedBox(height: 6),

          // Chapter & Subject
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
            decoration: BoxDecoration(
              color: AppColors.lightBlue,
              borderRadius: BorderRadius.circular(14),
            ),
            child: Text(
              '${certificate.localizedChapterTitle(lang)} • ${certificate.subjectName}',
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 15,
                fontWeight: FontWeight.bold,
                color: AppColors.darkBlue,
              ),
            ),
          ),
          const SizedBox(height: 14),

          // Details row
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              Column(
                children: [
                  const Text('Score', style: TextStyle(fontSize: 11, color: AppColors.textMuted)),
                  Text(
                    '${certificate.scorePercentage}% ⭐',
                    style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: AppColors.meadowGreen),
                  ),
                ],
              ),
              Column(
                children: [
                  const Text('Date', style: TextStyle(fontSize: 11, color: AppColors.textMuted)),
                  Text(
                    certificate.issueDate,
                    style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: AppColors.textDark),
                  ),
                ],
              ),
              Column(
                children: [
                  const Text('Seal', style: TextStyle(fontSize: 11, color: AppColors.textMuted)),
                  const Text(
                    'Bala Buddy 🤖',
                    style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: AppColors.coralOrange),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            'ID: ${certificate.certificateId}',
            style: const TextStyle(fontSize: 10, color: AppColors.textMuted, letterSpacing: 1),
          ),
        ],
      ),
    );
  }

  static void showCertificateDialog(BuildContext context, CertificateModel cert) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: Colors.transparent,
        contentPadding: EdgeInsets.zero,
        insetPadding: const EdgeInsets.all(16),
        content: CertificateWidget(certificate: cert),
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:baalavidya/l10n/app_strings.dart';
import 'package:baalavidya/widgets/pilot_feedback_dialog.dart';

void main() {
  group('Phase 11: Pilot, Beta and Launch Tests', () {
    test('Bilingual AppStrings covers all Phase 11 feedback keys without fallback', () {
      final keys = [
        'pilotFeedbackTitle',
        'pilotFeedbackSubtitle',
        'pilotRolePrompt',
        'pilotRoleStudent',
        'pilotRoleTeacher',
        'pilotRoleParent',
        'pilotRoleVolunteer',
        'pilotRatingPrompt',
        'pilotCommentPrompt',
        'pilotCommentPlaceholder',
        'pilotSubmitBtn',
        'pilotThankYouTitle',
        'pilotThankYouMessage',
        'pilotCloseBtn',
      ];

      for (final key in keys) {
        final enStr = AppStrings.get(key, 'en');
        final teStr = AppStrings.get(key, 'te');

        expect(enStr, isNotEmpty, reason: 'Key $key should exist in English');
        expect(teStr, isNotEmpty, reason: 'Key $key should exist in Telugu');
        expect(enStr, isNot(equals(key)), reason: 'Key $key should not return fallback in English');
        expect(teStr, isNot(equals(key)), reason: 'Key $key should not return fallback in Telugu');
        expect(enStr, isNot(equals(teStr)), reason: 'Key $key translation should be distinct');
      }
    });

    testWidgets('PilotFeedbackDialog renders and handles role selection and rating in English',
        (WidgetTester tester) async {
      Map<String, dynamic>? submittedData;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PilotFeedbackDialog(
              currentLanguage: 'en',
              onSubmit: (data) async {
                submittedData = data;
                return true;
              },
            ),
          ),
        ),
      );

      // Verify title and prompt
      expect(find.text(AppStrings.get('pilotFeedbackTitle', 'en')), findsOneWidget);
      expect(find.text(AppStrings.get('pilotRoleStudent', 'en')), findsOneWidget);
      expect(find.text(AppStrings.get('pilotRoleTeacher', 'en')), findsOneWidget);

      // Switch role to Teacher
      await tester.tap(find.byKey(const Key('chip_role_teacher')));
      await tester.pumpAndSettle();

      // Change star rating to 4 stars
      await tester.tap(find.byKey(const Key('pilot_star_4')));
      await tester.pumpAndSettle();

      // Enter feedback comment
      await tester.enterText(
        find.byKey(const Key('pilot_comment_field')),
        'The biology lesson diagrams helped my students understand photosynthesis deeply.',
      );
      await tester.pumpAndSettle();

      // Submit feedback
      await tester.tap(find.byKey(const Key('pilot_submit_btn')));
      await tester.pumpAndSettle();

      // Verify submitted data
      expect(submittedData, isNotNull);
      expect(submittedData!['stakeholder_role'], equals('teacher'));
      expect(submittedData!['rating'], equals(4));
      expect(submittedData!['comment'], contains('photosynthesis'));
      expect(submittedData!['language'], equals('en'));

      // Verify thank-you confirmation dialog appears
      expect(find.text(AppStrings.get('pilotThankYouTitle', 'en')), findsOneWidget);
      expect(find.text(AppStrings.get('pilotThankYouMessage', 'en')), findsOneWidget);
    });

    testWidgets('PilotFeedbackDialog renders properly in Telugu with volunteer role',
        (WidgetTester tester) async {
      Map<String, dynamic>? submittedData;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PilotFeedbackDialog(
              currentLanguage: 'te',
              onSubmit: (data) async {
                submittedData = data;
                return true;
              },
            ),
          ),
        ),
      );

      // Verify Telugu title
      expect(find.text(AppStrings.get('pilotFeedbackTitle', 'te')), findsOneWidget);
      expect(find.text(AppStrings.get('pilotRoleVolunteer', 'te')), findsOneWidget);

      // Switch to Vidya Volunteer
      await tester.tap(find.byKey(const Key('chip_role_volunteer')));
      await tester.pumpAndSettle();

      // Enter Telugu comment
      await tester.enterText(
        find.byKey(const Key('pilot_comment_field')),
        'పాఠశాల వై-ఫై హాట్‌స్పాట్ ద్వారా విద్యార్థుల ట్యాబ్లెట్‌లు వెంటనే సింక్ అయ్యాయి.',
      );
      await tester.pumpAndSettle();

      // Tap submit
      await tester.tap(find.byKey(const Key('pilot_submit_btn')));
      await tester.pumpAndSettle();

      expect(submittedData, isNotNull);
      expect(submittedData!['stakeholder_role'], equals('volunteer'));
      expect(submittedData!['rating'], equals(5));
      expect(submittedData!['language'], equals('te'));

      // Verify Telugu Thank You dialog
      expect(find.text(AppStrings.get('pilotThankYouTitle', 'te')), findsOneWidget);
      expect(find.text(AppStrings.get('pilotThankYouMessage', 'te')), findsOneWidget);
    });
  });
}

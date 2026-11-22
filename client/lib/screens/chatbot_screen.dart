import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/l10n/app_strings.dart';
import 'package:baalavidya/models/chat_models.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';
import 'package:baalavidya/widgets/language_toggle.dart';
import 'package:baalavidya/widgets/offline_banner.dart';

/// AI Chatbot screen adhering to [PS: 6. AI Chatbot; PS: 12. Bala Buddy].
/// Features:
/// 1. Friendly Bala Buddy persona (cheerful, encouraging, no jargon, no criticism).
/// 2. Bilingual interaction: answers in student's selected language (English or Telugu).
/// 3. Strict syllabus grounding with visible citation of retrieved textbook chunks.
/// 4. Kind decline behavior with related topics recommendations.
/// 5. Automatically logs each question into "Questions Asked" progress counter.
/// 6. Pre-populated quick question chips for easy tapping.
class ChatbotScreen extends ConsumerStatefulWidget {
  final String? initialQuery;

  const ChatbotScreen({
    super.key,
    this.initialQuery,
  });

  @override
  ConsumerState<ChatbotScreen> createState() => _ChatbotScreenState();
}

class _ChatbotScreenState extends ConsumerState<ChatbotScreen> {
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    if (widget.initialQuery != null && widget.initialQuery!.isNotEmpty) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        ref.read(chatMessagesProvider.notifier).sendQuestion(widget.initialQuery!);
      });
    }
  }

  @override
  void dispose() {
    _textController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void _handleSend([String? queryOverride]) {
    final text = queryOverride ?? _textController.text;
    if (text.trim().isEmpty) return;

    ref.read(chatMessagesProvider.notifier).sendQuestion(text.trim());
    _textController.clear();
    _scrollToBottom();
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);
    final messages = ref.watch(chatMessagesProvider);
    final questionsAsked = ref.watch(questionsAskedProvider);

    return Scaffold(
      backgroundColor: AppColors.softBackground,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        titleSpacing: 0,
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: const BoxDecoration(
                color: AppColors.lightGreen,
                shape: BoxShape.circle,
              ),
              child: const Text('🤖', style: TextStyle(fontSize: 24)),
            ),
            const SizedBox(width: 10),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  AppStrings.get('chatbotTitle', lang),
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: AppColors.textDark,
                  ),
                ),
                Text(
                  AppStrings.get('chatbotOnlineStatus', lang),
                  style: const TextStyle(fontSize: 12, color: AppColors.meadowGreen, fontWeight: FontWeight.w600),
                ),
              ],
            ),
          ],
        ),
        actions: [
          // Questions Asked Badge
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
            margin: const EdgeInsets.symmetric(vertical: 10),
            decoration: BoxDecoration(
              color: AppColors.lightYellow,
              borderRadius: BorderRadius.circular(14),
              border: Border.all(color: AppColors.sunshineYellow, width: 1.5),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text('❓', style: TextStyle(fontSize: 14)),
                const SizedBox(width: 4),
                Text(
                  '$questionsAsked',
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: AppColors.textDark,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(width: 4),
          const LanguageToggle(),
          const SizedBox(width: 8),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            const OfflineBanner(),
            // Quick Questions Chips Bar
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              color: Colors.white,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    AppStrings.get('quickQuestionsTitle', lang),
                    style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.bold,
                      color: AppColors.textMuted,
                    ),
                  ),
                  const SizedBox(height: 6),
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: [
                        _buildQuickChip(AppStrings.get('quickQ1', lang)),
                        const SizedBox(width: 8),
                        _buildQuickChip(AppStrings.get('quickQ2', lang)),
                        const SizedBox(width: 8),
                        _buildQuickChip(AppStrings.get('quickQ3', lang)),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const Divider(height: 1, color: AppColors.borderColor),

            // Messages List
            Expanded(
              child: ListView.builder(
                controller: _scrollController,
                padding: const EdgeInsets.all(16.0),
                itemCount: messages.length,
                itemBuilder: (context, index) {
                  final msg = messages[index];
                  return _buildMessageBubble(msg, lang);
                },
              ),
            ),

            // Input Bar
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
              decoration: BoxDecoration(
                color: Colors.white,
                border: const Border(top: BorderSide(color: AppColors.borderColor, width: 1.5)),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.04),
                    blurRadius: 4,
                    offset: const Offset(0, -2),
                  ),
                ],
              ),
              child: Row(
                children: [
                  Expanded(
                    child: Container(
                      height: 52,
                      decoration: BoxDecoration(
                        color: AppColors.softBackground,
                        borderRadius: BorderRadius.circular(26),
                        border: Border.all(color: AppColors.borderColor, width: 1.5),
                      ),
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      child: Row(
                        children: [
                          Expanded(
                            child: TextField(
                              controller: _textController,
                              onSubmitted: (_) => _handleSend(),
                              decoration: InputDecoration(
                                hintText: AppStrings.get('chatInputPlaceholder', lang),
                                hintStyle: const TextStyle(color: AppColors.textMuted, fontSize: 15),
                                border: InputBorder.none,
                              ),
                            ),
                          ),
                          IconButton(
                            icon: const Icon(Icons.mic_rounded, color: AppColors.coralOrange),
                            onPressed: () {
                              // Voice input placeholder
                            },
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  // Large Send Button
                  Container(
                    width: 52,
                    height: 52,
                    decoration: const BoxDecoration(
                      color: AppColors.primaryBlue,
                      shape: BoxShape.circle,
                    ),
                    child: IconButton(
                      icon: const Icon(Icons.send_rounded, color: Colors.white, size: 24),
                      onPressed: () => _handleSend(),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildQuickChip(String text) {
    return Container(
      constraints: const BoxConstraints(minHeight: 40),
      child: ActionChip(
        backgroundColor: AppColors.lightBlue,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: BorderSide(color: AppColors.primaryBlue.withOpacity(0.3)),
        ),
        label: Text(
          text,
          style: const TextStyle(
            fontSize: 13,
            fontWeight: FontWeight.w600,
            color: AppColors.darkBlue,
          ),
        ),
        onPressed: () => _handleSend(text),
      ),
    );
  }

  Widget _buildMessageBubble(ChatMessageModel msg, String lang) {
    final isUser = msg.isUser;

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!isUser) ...[
            Container(
              width: 38,
              height: 38,
              decoration: const BoxDecoration(
                color: AppColors.lightGreen,
                shape: BoxShape.circle,
              ),
              alignment: Alignment.center,
              child: const Text('🤖', style: TextStyle(fontSize: 20)),
            ),
            const SizedBox(width: 10),
          ],
          Flexible(
            child: Container(
              padding: const EdgeInsets.all(16.0),
              decoration: BoxDecoration(
                color: isUser ? AppColors.primaryBlue : Colors.white,
                borderRadius: BorderRadius.only(
                  topLeft: const Radius.circular(20),
                  topRight: const Radius.circular(20),
                  bottomLeft: isUser ? const Radius.circular(20) : Radius.zero,
                  bottomRight: isUser ? Radius.zero : const Radius.circular(20),
                ),
                border: Border.all(
                  color: isUser ? AppColors.primaryBlue : AppColors.borderColor,
                  width: 1.5,
                ),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.04),
                    blurRadius: 4,
                    offset: const Offset(0, 2),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    msg.text,
                    style: TextStyle(
                      fontSize: 16,
                      height: 1.45,
                      color: isUser ? Colors.white : AppColors.textDark,
                    ),
                  ),

                  // Grounded Textbook Citations Card
                  if (!isUser && msg.hasCitations) ...[
                    const SizedBox(height: 12),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                      decoration: BoxDecoration(
                        color: AppColors.lightGreen,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: AppColors.meadowGreen.withOpacity(0.4)),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(Icons.menu_book_rounded, color: AppColors.darkGreen, size: 18),
                          const SizedBox(width: 6),
                          Flexible(
                            child: Text(
                              '${AppStrings.get('syllabusSource', lang)} ${msg.syllabusChapter ?? "SCERT Textbook"} (Chunk: ${msg.citations.first.substring(0, 8)}...)',
                              style: const TextStyle(
                                fontSize: 12,
                                fontWeight: FontWeight.bold,
                                color: AppColors.darkGreen,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],

                  // Related Topics Recommendations (if question was out of syllabus)
                  if (!isUser && msg.isDeclined && msg.relatedTopics.isNotEmpty) ...[
                    const SizedBox(height: 12),
                    Text(
                      AppStrings.get('relatedTopics', lang),
                      style: const TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.bold,
                        color: AppColors.textDark,
                      ),
                    ),
                    const SizedBox(height: 6),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: msg.relatedTopics
                          .map(
                            (topic) => Padding(
                              padding: const EdgeInsets.only(top: 4.0),
                              child: InkWell(
                                onTap: () => _handleSend(topic),
                                child: Row(
                                  children: [
                                    const Text('👉 ', style: TextStyle(fontSize: 14)),
                                    Expanded(
                                      child: Text(
                                        topic,
                                        style: const TextStyle(
                                          fontSize: 14,
                                          color: AppColors.primaryBlue,
                                          fontWeight: FontWeight.w600,
                                          decoration: TextDecoration.underline,
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          )
                          .toList(),
                    ),
                  ],
                ],
              ),
            ),
          ),
          if (isUser) ...[
            const SizedBox(width: 10),
            Container(
              width: 38,
              height: 38,
              decoration: const BoxDecoration(
                color: AppColors.lightBlue,
                shape: BoxShape.circle,
              ),
              alignment: Alignment.center,
              child: const Text('🎒', style: TextStyle(fontSize: 20)),
            ),
          ],
        ],
      ),
    );
  }
}

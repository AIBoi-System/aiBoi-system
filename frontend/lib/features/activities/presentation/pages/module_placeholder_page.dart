import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:flutter/material.dart';

class ModulePlaceholderPage extends StatelessWidget {
  const ModulePlaceholderPage({
    super.key,
    required this.title,
    required this.rfCode,
    this.message,
    this.actionLabel,
    this.onAction,
  });

  final String title;
  final String rfCode;
  final String? message;
  final String? actionLabel;
  final VoidCallback? onAction;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: AppColors.primaryButton,
        foregroundColor: Colors.white,
        title: Text(title),
      ),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(
                color: AppColors.primaryButton.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                rfCode,
                style: const TextStyle(
                  color: AppColors.primaryButton,
                  fontWeight: FontWeight.w600,
                  fontSize: 12,
                ),
              ),
            ),
            const SizedBox(height: 20),
            Text(
              message ?? 'Funcionalidade em desenvolvimento.',
              style: const TextStyle(
                fontSize: 15,
                height: 1.5,
                color: AppColors.textPrimary,
                fontFamily: 'Poppins',
              ),
            ),
            const Spacer(),
            if (actionLabel != null && onAction != null)
              PrimaryButton(text: actionLabel!, onPressed: onAction),
          ],
        ),
      ),
    );
  }
}


import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:flutter/material.dart';

class PasswordRules {
  final bool minLength;
  final bool hasNumber;
  final bool hasSymbol;

  const PasswordRules({
    required this.minLength,
    required this.hasNumber,
    required this.hasSymbol,
  });

  factory PasswordRules.fromPassword(String password) {
    return PasswordRules(
      minLength: password.length >= 8,
      hasNumber: RegExp(r'\d').hasMatch(password),
      hasSymbol: RegExp(
        r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;/]',
      ).hasMatch(password),
    );
  }

  bool get allMet => minLength && hasNumber && hasSymbol;

  double get strengthFraction {
    var score = 0;
    if (minLength) score++;
    if (hasNumber) score++;
    if (hasSymbol) score++;
    return score / 3;
  }

  Color get strengthColor {
    if (strengthFraction < 0.34) return AppColors.strengthWeak;
    if (strengthFraction < 1) return AppColors.strengthMedium;
    return AppColors.strengthStrong;
  }
}

class PasswordStrengthIndicator extends StatelessWidget {
  final PasswordRules rules;

  const PasswordStrengthIndicator({super.key, required this.rules});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 8),
        ClipRRect(
          borderRadius: BorderRadius.circular(4),
          child: LinearProgressIndicator(
            value: rules.strengthFraction,
            minHeight: 4,
            backgroundColor: AppColors.progressInactive,
            color: rules.strengthColor,
          ),
        ),
        const SizedBox(height: 16),
        _RuleRow(met: rules.minLength, text: '8 caracteres no mínimo'),
        const SizedBox(height: 8),
        _RuleRow(met: rules.hasNumber, text: 'Um número'),
        const SizedBox(height: 8),
        _RuleRow(met: rules.hasSymbol, text: 'Um símbolo'),
      ],
    );
  }
}

class _RuleRow extends StatelessWidget {
  final bool met;
  final String text;

  const _RuleRow({required this.met, required this.text});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(
          met ? Icons.check_circle : Icons.radio_button_unchecked,
          size: 20,
          color: met ? AppColors.progressActive : Colors.grey.shade400,
        ),
        const SizedBox(width: 8),
        Text(
          text,
          style: TextStyle(
            fontSize: 14,
            color: met ? AppColors.textPrimary : AppColors.textSecondary,
            fontFamily: 'Poppins',
          ),
        ),
      ],
    );
  }
}

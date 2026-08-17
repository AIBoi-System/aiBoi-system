import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/core/widgets/signup_step_scaffold.dart';
import 'package:flutter/material.dart';

class AuthMethodScaffold extends StatelessWidget {
  const AuthMethodScaffold({
    super.key,
    required this.title,
    required this.subtitle,
    required this.onEmail,
    required this.onGoogle,
    required this.onApple,
    this.googleLoading = false,
  });

  final String title;
  final String subtitle;
  final VoidCallback onEmail;
  final VoidCallback onGoogle;
  final VoidCallback onApple;
  final bool googleLoading;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: AuthPageFrame(
        child: SafeArea(
          child: Column(
            children: [
              AuthHeader(title: title),
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.fromLTRB(16, 24, 16, 40),
                  child: Column(
                    children: [
                      Align(
                        alignment: Alignment.centerLeft,
                        child: Text(
                          subtitle,
                          style: const TextStyle(
                            color: AppColors.textPrimary,
                            fontFamily: 'Roboto',
                            fontSize: 16,
                            height: 1.6,
                          ),
                        ),
                      ),
                      const SizedBox(height: 32),
                      PrimaryButton(
                        text: 'Continue com e-mail',
                        onPressed: onEmail,
                      ),
                      const SizedBox(height: 20),
                      const Text(
                        'ou',
                        style: TextStyle(
                          color: AppColors.textSecondary,
                          fontFamily: 'Roboto',
                          fontSize: 16,
                          fontWeight: FontWeight.w500,
                          height: 1.6,
                        ),
                      ),
                      const SizedBox(height: 20),
                      SocialAuthButton(
                        label: 'Continue com Apple',
                        icon: const Icon(
                          Icons.apple,
                          size: 20,
                          color: Color(0xFF3A383F),
                        ),
                        onPressed: onApple,
                      ),
                      const SizedBox(height: 12),
                      SocialAuthButton(
                        label: googleLoading
                            ? 'Conectando...'
                            : 'Continue com Google',
                        icon: Image.asset(
                          'assets/images/google_logo.png',
                          width: 20,
                          height: 20,
                          fit: BoxFit.contain,
                        ),
                        onPressed: googleLoading ? null : onGoogle,
                      ),
                      const Spacer(),
                      const Text.rich(
                        TextSpan(
                          text: 'Ao usar o AgroFence, você concorda com os\n',
                          children: [
                            TextSpan(
                              text: 'Termos',
                              style: TextStyle(fontWeight: FontWeight.w600),
                            ),
                            TextSpan(text: ' e '),
                            TextSpan(
                              text: 'Política de Privacidade',
                              style: TextStyle(fontWeight: FontWeight.w600),
                            ),
                            TextSpan(text: '.'),
                          ],
                        ),
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: AppColors.textSecondary,
                          fontFamily: 'Roboto',
                          fontSize: 14,
                          height: 1.6,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class SocialAuthButton extends StatelessWidget {
  const SocialAuthButton({
    super.key,
    required this.label,
    required this.icon,
    required this.onPressed,
  });

  final String label;
  final Widget icon;
  final VoidCallback? onPressed;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      height: 60,
      child: OutlinedButton.icon(
        onPressed: onPressed,
        icon: SizedBox(width: 20, height: 20, child: icon),
        label: Text(label),
        style: ButtonStyle(
          foregroundColor: const WidgetStatePropertyAll(Color(0xFF3A383F)),
          backgroundColor: WidgetStateProperty.resolveWith((states) {
            if (states.contains(WidgetState.hovered)) {
              return AppColors.backgroundScreen;
            }
            return Colors.white;
          }),
          side: const WidgetStatePropertyAll(
            BorderSide(color: AppColors.border),
          ),
          shape: WidgetStatePropertyAll(
            RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          ),
          textStyle: const WidgetStatePropertyAll(
            TextStyle(
              fontFamily: 'Roboto',
              fontSize: 14,
              fontWeight: FontWeight.w500,
            ),
          ),
        ),
      ),
    );
  }
}

import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/core/widgets/signup_step_scaffold.dart';
import 'package:flutter/material.dart';

class SignupEntryPage extends StatelessWidget {
  const SignupEntryPage({super.key});

  @override
  Widget build(BuildContext context) {
    return SignupSimpleScaffold(
      title: 'Acesse sua conta',
      subtitle:
          'Comece com uma conta gratuita e veja como é fácil ter o controle total da sua fazenda na palma da mão!',
      bottom: Column(
        children: [
          PrimaryButton(
            text: 'Continue com e-mail',
            onPressed: () {
              AppRouter.navigateRegistration(context, AppRouter.signupPersonal);
            },
          ),
          const SizedBox(height: 16),
          const Text(
            'ou',
            style: TextStyle(color: AppColors.textSecondary, fontFamily: 'Poppins'),
          ),
          const SizedBox(height: 16),
          _SocialButton(
            icon: Icons.apple,
            label: 'Continue com Apple',
            onPressed: () {},
          ),
          const SizedBox(height: 12),
          _SocialButton(
            icon: Icons.g_mobiledata,
            label: 'Continue com Google',
            onPressed: () {},
          ),
          const SizedBox(height: 24),
          const Center(
            child: Text(
              'Ao usar o Ai Boi, você concorda com os\nTermos e Política de Privacidade.',
              textAlign: TextAlign.center,
              style: TextStyle(
                color: AppColors.textSecondary,
                fontSize: 12,
                fontFamily: 'Poppins',
              ),
            ),
          ),
        ],
      ),
      child: const SizedBox.shrink(),
    );
  }
}

class _SocialButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onPressed;

  const _SocialButton({
    required this.icon,
    required this.label,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      height: 50,
      child: OutlinedButton.icon(
        onPressed: onPressed,
        icon: Icon(icon, color: Colors.black87),
        label: Text(
          label,
          style: const TextStyle(
            color: Colors.black87,
            fontWeight: FontWeight.w500,
            fontFamily: 'Poppins',
          ),
        ),
        style: OutlinedButton.styleFrom(
          side: BorderSide(color: Colors.grey.shade300),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        ),
      ),
    );
  }
}


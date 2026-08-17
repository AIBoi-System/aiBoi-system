import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:flutter/material.dart';

class SignupCompletePage extends StatelessWidget {
  const SignupCompletePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            children: [
              const Spacer(),
              Container(
                width: 80,
                height: 80,
                decoration: BoxDecoration(
                  color: AppColors.progressActive.withValues(alpha: 0.2),
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.check,
                  color: AppColors.progressActive,
                  size: 48,
                ),
              ),
              const SizedBox(height: 24),
              const Text(
                'Cadastro concluído!',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: AppColors.primaryGreen,
                  fontFamily: 'Poppins',
                ),
              ),
              const SizedBox(height: 12),
              const Text(
                'Sua conta foi criada com sucesso. Agora você precisa cadastrar sua primeira propriedade.',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 14,
                  color: AppColors.textSecondary,
                  height: 1.4,
                  fontFamily: 'Poppins',
                ),
              ),
              const Spacer(),
              PrimaryButton(
                text: 'Cadastrar propriedade',
                onPressed: () {
                  AppRouter.navigateRegistration(
                    context,
                    AppRouter.propertyCreate,
                  );
                },
              ),

            ],
          ),
        ),
      ),
    );
  }
}

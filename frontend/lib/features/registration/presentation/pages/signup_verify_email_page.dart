import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/otp_code_field.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/core/widgets/signup_step_scaffold.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_cubit.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_state.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class SignupVerifyEmailPage extends StatefulWidget {
  const SignupVerifyEmailPage({super.key});

  @override
  State<SignupVerifyEmailPage> createState() => _SignupVerifyEmailPageState();
}

class _SignupVerifyEmailPageState extends State<SignupVerifyEmailPage> {
  String _code = '';

  @override
  Widget build(BuildContext context) {
    final email = context.read<RegistrationCubit>().email;

    return BlocConsumer<RegistrationCubit, RegistrationState>(
      listener: (context, state) {
        if (state is RegistrationEmailVerified) {
          AppRouter.navigateRegistration(context, AppRouter.signupPassword);
        } else if (state is RegistrationError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message), backgroundColor: Colors.red),
          );
        }
      },
      builder: (context, state) {
        final isLoading = state is RegistrationLoading;
        return SignupStepScaffold(
          title: 'Verifique seu email',
          currentStep: 2,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Verifique seu e-mail. Enviamos um código de confirmação para $email:',
                style: const TextStyle(
                  color: AppColors.textSecondary,
                  fontSize: 14,
                  height: 1.4,
                  fontFamily: 'Poppins',
                ),
              ),
              const SizedBox(height: 24),
              OtpCodeField(
                onChanged: (c) => _code = c,
                onCompleted: (c) => _code = c,
              ),
              const SizedBox(height: 16),
              Center(
                child: TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text.rich(
                    TextSpan(
                      text: 'E-mail incorreto? ',
                      style: TextStyle(
                        color: AppColors.textSecondary,
                        fontFamily: 'Poppins',
                      ),
                      children: [
                        TextSpan(
                          text: 'Alterar e-mail',
                          style: TextStyle(
                            color: Colors.black,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
          bottom: PrimaryButton(
            text: isLoading ? 'Verificando...' : 'Verificar email',
            onPressed: isLoading || _code.length < 5
                ? null
                : () => context.read<RegistrationCubit>().verifyCode(_code),
          ),
        );
      },
    );
  }
}

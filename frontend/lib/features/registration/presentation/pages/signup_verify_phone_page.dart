import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/widgets/otp_code_field.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/core/widgets/signup_step_scaffold.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_cubit.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_state.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class SignupVerifyPhonePage extends StatefulWidget {
  const SignupVerifyPhonePage({super.key});

  @override
  State<SignupVerifyPhonePage> createState() => _SignupVerifyPhonePageState();
}

class _SignupVerifyPhonePageState extends State<SignupVerifyPhonePage> {
  String _code = '';

  @override
  Widget build(BuildContext context) {
    final phone = context.read<RegistrationCubit>().phone ?? '';
    return BlocConsumer<RegistrationCubit, RegistrationState>(
      listener: (context, state) {
        if (state is RegistrationPhoneVerified) {
          AppRouter.navigateRegistration(context, AppRouter.signupAddress);
        } else if (state is RegistrationError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message), backgroundColor: Colors.red),
          );
        }
      },
      builder: (context, state) {
        final isLoading = state is RegistrationLoading;
        return SignupStepScaffold(
          title: 'Confirme seu telefone',
          currentStep: 4,
          totalSteps: 6,
          bottom: PrimaryButton(
            text: 'Confirmar telefone',
            isLoading: isLoading,
            onPressed: isLoading || _code.length != 5
                ? null
                : () =>
                      context.read<RegistrationCubit>().verifyPhoneCode(_code),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Enviamos um código de confirmação para $phone.'),
              const SizedBox(height: 24),
              OtpCodeField(
                onChanged: (value) => setState(() => _code = value),
                onCompleted: (value) {
                  setState(() => _code = value);
                  context.read<RegistrationCubit>().verifyPhoneCode(value);
                },
              ),
            ],
          ),
        );
      },
    );
  }
}

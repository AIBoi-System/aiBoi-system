import 'package:ai_boi/core/widgets/labeled_text_field.dart';
import 'package:ai_boi/core/widgets/password_strength_indicator.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/core/widgets/signup_step_scaffold.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_cubit.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_state.dart';
import 'package:ai_boi/features/registration/presentation/pages/signup_complete_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class SignupPasswordPage extends StatefulWidget {
  const SignupPasswordPage({super.key});

  @override
  State<SignupPasswordPage> createState() => _SignupPasswordPageState();
}

class _SignupPasswordPageState extends State<SignupPasswordPage> {
  final _passwordController = TextEditingController();
  bool _obscure = true;

  @override
  void dispose() {
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final rules = PasswordRules.fromPassword(_passwordController.text);
    return BlocConsumer<RegistrationCubit, RegistrationState>(
      listener: (context, state) {
        if (state is RegistrationUserCreated) {
          final cubit = context.read<RegistrationCubit>();
          Navigator.pushAndRemoveUntil(
            context,
            MaterialPageRoute(
              builder: (_) => BlocProvider.value(
                value: cubit,
                child: const SignupCompletePage(),
              ),
            ),
            (route) => route.isFirst,
          );
        } else if (state is RegistrationError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message), backgroundColor: Colors.red),
          );
        }
      },
      builder: (context, state) {
        final isLoading = state is RegistrationLoading;
        return SignupStepScaffold(
          title: 'Crie sua senha',
          currentStep: 6,
          totalSteps: 6,
          bottom: PrimaryButton(
            text: 'Concluir cadastro',
            isLoading: isLoading,
            onPressed: isLoading || !rules.allMet
                ? null
                : () {
                    final cubit = context.read<RegistrationCubit>();
                    cubit.password = _passwordController.text;
                    cubit.completeRegistration();
                  },
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              LabeledTextField(
                label: 'Senha',
                hintText: '••••••••',
                controller: _passwordController,
                obscureText: _obscure,
                onChanged: (_) => setState(() {}),
                suffixIcon: IconButton(
                  icon: Icon(
                    _obscure
                        ? Icons.visibility_off_outlined
                        : Icons.visibility_outlined,
                    color: Colors.grey,
                  ),
                  onPressed: () => setState(() => _obscure = !_obscure),
                ),
              ),
              PasswordStrengthIndicator(rules: rules),
            ],
          ),
        );
      },
    );
  }
}

import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/widgets/labeled_text_field.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/core/widgets/signup_step_scaffold.dart';
import 'package:ai_boi/features/registration/domain/registration_validators.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_cubit.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_state.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class SignupPersonalPage extends StatefulWidget {
  const SignupPersonalPage({super.key});

  @override
  State<SignupPersonalPage> createState() => _SignupPersonalPageState();
}

class _SignupPersonalPageState extends State<SignupPersonalPage> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _emailController.text = context.read<RegistrationCubit>().email;
  }

  @override
  void dispose() {
    _emailController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<RegistrationCubit, RegistrationState>(
      listener: (context, state) {
        if (state is RegistrationCodeSent) {
          AppRouter.navigateRegistration(context, AppRouter.signupVerifyEmail);
        } else if (state is RegistrationError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message), backgroundColor: Colors.red),
          );
        }
      },
      builder: (context, state) {
        final isLoading = state is RegistrationLoading;
        return SignupStepScaffold(
          title: 'Seu e-mail',
          currentStep: 1,
          totalSteps: 6,
          bottom: PrimaryButton(
            text: 'Enviar código',
            isLoading: isLoading,
            onPressed: isLoading
                ? null
                : () {
                    if (_formKey.currentState!.validate()) {
                      final cubit = context.read<RegistrationCubit>();
                      cubit.email = _emailController.text;
                      cubit.sendVerificationCode();
                    }
                  },
          ),
          child: Form(
            key: _formKey,
            child: LabeledTextField(
              label: 'E-mail',
              hintText: 'seu@email.com',
              controller: _emailController,
              keyboardType: TextInputType.emailAddress,
              validator: RegistrationValidators.email,
            ),
          ),
        );
      },
    );
  }
}

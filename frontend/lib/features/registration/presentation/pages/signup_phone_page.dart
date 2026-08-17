import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/widgets/labeled_text_field.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/core/widgets/signup_step_scaffold.dart';
import 'package:ai_boi/features/registration/domain/registration_validators.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_cubit.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_state.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class SignupPhonePage extends StatefulWidget {
  const SignupPhonePage({super.key});

  @override
  State<SignupPhonePage> createState() => _SignupPhonePageState();
}

class _SignupPhonePageState extends State<SignupPhonePage> {
  final _formKey = GlobalKey<FormState>();
  final _phoneController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _phoneController.text = context.read<RegistrationCubit>().phone ?? '';
  }

  @override
  void dispose() {
    _phoneController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<RegistrationCubit, RegistrationState>(
      listener: (context, state) {
        if (state is RegistrationPhoneCodeSent) {
          AppRouter.navigateRegistration(context, AppRouter.signupVerifyPhone);
        } else if (state is RegistrationError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message), backgroundColor: Colors.red),
          );
        }
      },
      builder: (context, state) {
        final isLoading = state is RegistrationLoading;
        return SignupStepScaffold(
          title: 'Seu telefone',
          currentStep: 3,
          totalSteps: 6,
          bottom: PrimaryButton(
            text: 'Enviar código',
            isLoading: isLoading,
            onPressed: isLoading
                ? null
                : () {
                    if (_formKey.currentState!.validate()) {
                      context
                          .read<RegistrationCubit>()
                          .sendPhoneVerificationCode(_phoneController.text);
                    }
                  },
          ),
          child: Form(
            key: _formKey,
            child: LabeledTextField(
              label: 'Telefone com DDD',
              hintText: '11999999999',
              controller: _phoneController,
              keyboardType: TextInputType.phone,
              inputFormatters: [
                FilteringTextInputFormatter.digitsOnly,
                LengthLimitingTextInputFormatter(11),
              ],
              validator: RegistrationValidators.phone,
            ),
          ),
        );
      },
    );
  }
}

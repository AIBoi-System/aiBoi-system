import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/widgets/labeled_text_field.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/core/widgets/signup_step_scaffold.dart';
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
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();

  @override
  void dispose() {
    _nameController.dispose();
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
          title: 'Dados Pessoais',
          currentStep: 1,
          bottom: PrimaryButton(
            text: isLoading ? 'Enviando...' : 'Criar minha conta',
            onPressed: isLoading
                ? null
                : () {
                    if (_formKey.currentState!.validate()) {
                      final cubit = context.read<RegistrationCubit>();
                      cubit.name = _nameController.text.trim();
                      cubit.email = _emailController.text.trim();
                      cubit.sendVerificationCode();
                    }
                  },
          ),
          child: Form(
            key: _formKey,
            child: Column(
              children: [
                LabeledTextField(
                  label: 'Nome',
                  hintText: 'Seu nome completo',
                  controller: _nameController,
                  validator: (v) =>
                      v == null || v.trim().length < 3 ? 'Informe seu nome' : null,
                ),
                const SizedBox(height: 20),
                LabeledTextField(
                  label: 'E-mail',
                  hintText: 'seu@email.com',
                  controller: _emailController,
                  keyboardType: TextInputType.emailAddress,
                  validator: (v) {
                    if (v == null || v.isEmpty) return 'Informe o e-mail';
                    if (!v.contains('@')) return 'E-mail inválido';
                    return null;
                  },
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}


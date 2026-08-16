import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/labeled_text_field.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/core/widgets/signup_step_scaffold.dart';
import 'package:ai_boi/features/auth/presentation/cubits/login_cubit.dart';
import 'package:ai_boi/features/auth/presentation/cubits/login_state.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<LoginCubit, LoginState>(
      listener: (context, state) {
        if (state is LoginSuccess) {
          Navigator.pushNamedAndRemoveUntil(
            context,
            AppRouter.properties,
            (route) => false,
          );
        } else if (state is LoginError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message), backgroundColor: Colors.red),
          );
        }
      },
      builder: (context, state) {
        final isLoading = state is LoginLoading;
        return Scaffold(
          backgroundColor: Colors.white,
          body: AuthPageFrame(
            child: SafeArea(
              child: Column(
                children: [
                  const AuthHeader(title: 'Entrar com e-mail'),
                  Expanded(
                    child: SingleChildScrollView(
                      keyboardDismissBehavior:
                          ScrollViewKeyboardDismissBehavior.onDrag,
                      padding: const EdgeInsets.fromLTRB(16, 24, 16, 24),
                      child: Form(
                        key: _formKey,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Digite os dados usados no cadastro.',
                              style: TextStyle(
                                color: AppColors.textPrimary,
                                fontFamily: 'Roboto',
                                fontSize: 16,
                                height: 1.6,
                              ),
                            ),
                            const SizedBox(height: 32),
                            LabeledTextField(
                              label: 'E-mail',
                              hintText: 'seu@email.com',
                              controller: _emailController,
                              keyboardType: TextInputType.emailAddress,
                              validator: (value) {
                                final email = value?.trim() ?? '';
                                if (email.isEmpty) {
                                  return 'Informe seu e-mail';
                                }
                                final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
                                if (!emailRegex.hasMatch(email)) {
                                  return 'E-mail inválido';
                                }
                                return null;
                              },
                            ),
                            const SizedBox(height: 20),
                            LabeledTextField(
                              label: 'Senha',
                              hintText: 'Digite sua senha',
                              controller: _passwordController,
                              obscureText: _obscurePassword,
                              suffixIcon: IconButton(
                                icon: Icon(
                                  _obscurePassword
                                      ? Icons.visibility_off_outlined
                                      : Icons.visibility_outlined,
                                  color: AppColors.textSecondary,
                                ),
                                onPressed: () => setState(
                                  () => _obscurePassword = !_obscurePassword,
                                ),
                              ),
                              validator: (value) {
                                if (value == null || value.isEmpty) {
                                  return 'Informe sua senha';
                                }
                                return null;
                              },
                            ),
                            Align(
                              alignment: Alignment.centerRight,
                              child: TextButton(
                                onPressed: () =>
                                    ScaffoldMessenger.of(context).showSnackBar(
                                      const SnackBar(
                                        content: Text(
                                          'Recuperação de senha será aberta aqui.',
                                        ),
                                      ),
                                    ),
                                child: const Text(
                                  'Esqueceu a senha?',
                                  style: TextStyle(
                                    color: AppColors.primaryGreen,
                                    fontFamily: 'Roboto',
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                              ),
                            ),
                            const SizedBox(height: 20),
                            PrimaryButton(
                              text: 'Entrar',
                              isLoading: isLoading,
                              onPressed: isLoading ? null : _submit,
                            ),
                            const SizedBox(height: 16),
                            Center(
                              child: TextButton(
                                onPressed: () => Navigator.maybePop(context),
                                child: const Text(
                                  'Usar outra forma de acesso',
                                  style: TextStyle(
                                    color: AppColors.primaryGreen,
                                    fontFamily: 'Roboto',
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  void _submit() {
    if (!_formKey.currentState!.validate()) return;
    context.read<LoginCubit>().signIn(
      _emailController.text.trim(),
      _passwordController.text,
    );
  }
}

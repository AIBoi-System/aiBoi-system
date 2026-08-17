import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/widgets/auth_method_scaffold.dart';
import 'package:ai_boi/features/auth/presentation/cubits/login_cubit.dart';
import 'package:ai_boi/features/auth/presentation/cubits/login_state.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_cubit.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class LoginOptionsPage extends StatelessWidget {
  const LoginOptionsPage({super.key});

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
        } else if (state is GoogleLoginNeedsRegistration) {
          final registration = context.read<RegistrationCubit>();
          registration.beginGoogleRegistration(
            email: state.email,
            name: state.name ?? '',
            idToken: state.idToken,
          );
          AppRouter.navigateRegistration(context, AppRouter.signupPhone);
        } else if (state is LoginError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message), backgroundColor: Colors.red),
          );
        }
      },
      builder: (context, state) {
        return AuthMethodScaffold(
          title: 'Acesse sua conta',
          subtitle:
              'Entre com seu e-mail e senha ou continue com sua conta Google.',
          googleLoading: state is LoginLoading,
          onEmail: () => Navigator.pushNamed(context, AppRouter.loginEmail),
          onGoogle: () => context.read<LoginCubit>().signInWithGoogle(),
          onApple: () => _showAppleUnavailable(context),
        );
      },
    );
  }

  void _showAppleUnavailable(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Login com Apple estará disponível em breve.'),
      ),
    );
  }
}

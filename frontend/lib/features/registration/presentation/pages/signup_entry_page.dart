import 'package:ai_boi/core/di/app_bindings.dart';
import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/widgets/auth_method_scaffold.dart';
import 'package:ai_boi/features/auth/presentation/cubits/login_cubit.dart';
import 'package:ai_boi/features/auth/presentation/cubits/login_state.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_cubit.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class SignupEntryPage extends StatelessWidget {
  const SignupEntryPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => AppBindings.createLoginCubit(),
      child: BlocConsumer<LoginCubit, LoginState>(
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
              SnackBar(
                content: Text(state.message),
                backgroundColor: Colors.red,
              ),
            );
          }
        },
        builder: (context, state) {
          return AuthMethodScaffold(
            title: 'Crie sua conta',
            subtitle:
                'Comece com uma conta gratuita e veja como é fácil ter o controle total da sua fazenda na palma da mão!',
            googleLoading: state is LoginLoading,
            onEmail: () => AppRouter.navigateRegistration(
              context,
              AppRouter.signupPersonal,
            ),
            onGoogle: () => context.read<LoginCubit>().signInWithGoogle(),
            onApple: () => ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('Cadastro com Apple estará disponível em breve.'),
              ),
            ),
          );
        },
      ),
    );
  }
}

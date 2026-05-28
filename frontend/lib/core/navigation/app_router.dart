import 'package:ai_boi/core/di/app_bindings.dart';
import 'package:ai_boi/features/auth/presentation/pages/login_page.dart';
import 'package:ai_boi/features/auth/presentation/pages/welcome_page.dart';
import 'package:ai_boi/features/home/presentation/pages/home_page.dart';
import 'package:ai_boi/features/property/presentation/pages/property_form_page.dart';
import 'package:ai_boi/features/property/presentation/pages/property_success_page.dart';
import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_cubit.dart';
import 'package:ai_boi/features/registration/presentation/pages/signup_address_page.dart';
import 'package:ai_boi/features/registration/presentation/pages/signup_complete_page.dart';
import 'package:ai_boi/features/registration/presentation/pages/signup_entry_page.dart';
import 'package:ai_boi/features/registration/presentation/pages/signup_password_page.dart';
import 'package:ai_boi/features/registration/presentation/pages/signup_personal_page.dart';
import 'package:ai_boi/features/registration/presentation/pages/signup_verify_email_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class AppRouter {
  static const String welcome = '/';
  static const String login = '/login';
  static const String signup = '/signup';
  static const String signupPersonal = '/signup/personal';
  static const String signupVerifyEmail = '/signup/verify-email';
  static const String signupPassword = '/signup/password';
  static const String signupAddress = '/signup/address';
  static const String signupComplete = '/signup/complete';
  static const String propertyCreate = '/property/create';
  static const String propertySuccess = '/property/success';
  static const String home = '/home';
  static const String dashboard = '/dashboard';

  static void navigateRegistration(BuildContext context, String routeName) {
    final cubit = context.read<RegistrationCubit>();
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => BlocProvider.value(
          value: cubit,
          child: _registrationPage(routeName),
        ),
      ),
    );
  }

  static Widget _registrationPage(String routeName) {
    switch (routeName) {
      case signupPersonal:
        return const SignupPersonalPage();
      case signupVerifyEmail:
        return const SignupVerifyEmailPage();
      case signupPassword:
        return const SignupPasswordPage();
      case signupAddress:
        return const SignupAddressPage();
      case propertyCreate:
        return const PropertyFormPage();
      default:
        return const SignupEntryPage();
    }
  }

  static Route<dynamic> onGenerateRoute(RouteSettings settings) {
    switch (settings.name) {
      case welcome:
        return MaterialPageRoute(builder: (_) => const WelcomePage());
      case login:
        return MaterialPageRoute(
          builder: (_) => BlocProvider(
            create: (_) => AppBindings.createLoginCubit(),
            child: const LoginPage(),
          ),
        );
      case signup:
        return MaterialPageRoute(
          builder: (_) => BlocProvider(
            create: (_) => AppBindings.createRegistrationCubit(),
            child: const SignupEntryPage(),
          ),
        );
      case signupComplete:
        return MaterialPageRoute(builder: (_) => const SignupCompletePage());
      case propertySuccess:
        return MaterialPageRoute(
          builder: (_) => const PropertySuccessPage(),
          settings: settings,
        );
      case home:
        return MaterialPageRoute(
          builder: (_) => HomePage(
            properties: settings.arguments is List<RegisteredProperty>
                ? settings.arguments as List<RegisteredProperty>
                : settings.arguments is RegisteredProperty
                    ? [settings.arguments as RegisteredProperty]
                    : const [],
          ),
          settings: settings,
        );
      default:
        return MaterialPageRoute(builder: (_) => const WelcomePage());
    }
  }

}

import 'package:ai_boi/core/di/app_bindings.dart';
import 'package:ai_boi/features/auth/presentation/pages/login_page.dart';
import 'package:ai_boi/features/auth/presentation/pages/login_options_page.dart';
import 'package:ai_boi/features/auth/presentation/pages/welcome_page.dart';
import 'package:ai_boi/features/home/presentation/pages/home_page.dart';
import 'package:ai_boi/features/dashboard/presentation/pages/dashboard_page.dart';
import 'package:ai_boi/features/activities/presentation/pages/activities_page.dart';
import 'package:ai_boi/features/profile/presentation/pages/profile_page.dart';
import 'package:ai_boi/features/property/presentation/pages/property_form_page.dart';
import 'package:ai_boi/features/property/presentation/pages/properties_page.dart';
import 'package:ai_boi/features/property/presentation/pages/property_success_page.dart';
import 'package:ai_boi/features/settings/presentation/pages/settings_page.dart';
import 'package:ai_boi/features/modules/presentation/pages/modules_page.dart';
import 'package:ai_boi/features/modules/presentation/pages/module_store_page.dart';
import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_cubit.dart';
import 'package:ai_boi/features/registration/presentation/pages/signup_address_page.dart';
import 'package:ai_boi/features/registration/presentation/pages/signup_complete_page.dart';
import 'package:ai_boi/features/registration/presentation/pages/signup_entry_page.dart';
import 'package:ai_boi/features/registration/presentation/pages/signup_password_page.dart';
import 'package:ai_boi/features/registration/presentation/pages/signup_personal_page.dart';
import 'package:ai_boi/features/registration/presentation/pages/signup_phone_page.dart';
import 'package:ai_boi/features/registration/presentation/pages/signup_verify_email_page.dart';
import 'package:ai_boi/features/registration/presentation/pages/signup_verify_phone_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class AppRouter {
  static const String welcome = '/';
  static const String login = '/login';
  static const String loginEmail = '/login/email';
  static const String signup = '/signup';
  static const String signupPersonal = '/signup/personal';
  static const String signupVerifyEmail = '/signup/verify-email';
  static const String signupPhone = '/signup/phone';
  static const String signupVerifyPhone = '/signup/verify-phone';
  static const String signupPassword = '/signup/password';
  static const String signupAddress = '/signup/address';
  static const String signupComplete = '/signup/complete';
  static const String propertyCreate = '/property/create';
  static const String propertySuccess = '/property/success';
  static const String home = '/home';
  static const String properties = '/properties';
  static const String activities = '/activities';
  static const String appSettings = '/settings';
  static const String profile = '/profile';
  static const String dashboard = '/dashboard';
  static const String modules = '/modules';
  static const String moduleStore = '/module-store';

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
      case signupPhone:
        return const SignupPhonePage();
      case signupVerifyPhone:
        return const SignupVerifyPhonePage();
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
          builder: (_) => MultiBlocProvider(
            providers: [
              BlocProvider(create: (_) => AppBindings.createLoginCubit()),
              BlocProvider(
                create: (_) => AppBindings.createRegistrationCubit(),
              ),
            ],
            child: const LoginOptionsPage(),
          ),
        );
      case loginEmail:
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
      case propertyCreate:
        return MaterialPageRoute(
          builder: (_) => BlocProvider(
            create: (_) => AppBindings.createRegistrationCubit(),
            child: const PropertyFormPage(),
          ),
        );
      case propertySuccess:
        return MaterialPageRoute(
          builder: (_) => const PropertySuccessPage(),
          settings: settings,
        );
      case home:
        return MaterialPageRoute(
          builder: (_) => HomePage(
            property: settings.arguments is RegisteredProperty
                ? settings.arguments as RegisteredProperty
                : null,
          ),
          settings: settings,
        );
      case properties:
        return MaterialPageRoute(builder: (_) => const PropertiesPage());
      case activities:
        final args = settings.arguments is Map<String, dynamic>
            ? settings.arguments as Map<String, dynamic>
            : const <String, dynamic>{};
        return MaterialPageRoute(
          builder: (_) => ActivitiesPage(
            propertyId: args['propertyId'] as int? ?? 1,
            propertyName: args['propertyName'] as String? ?? 'Sabiá Dourado',
            operations: AppBindings.operations(),
          ),
        );
      case appSettings:
        return MaterialPageRoute(builder: (_) => const SettingsPage());
      case profile:
        return MaterialPageRoute(
          builder: (_) => ProfilePage(
            initialTab: settings.arguments is int
                ? settings.arguments as int
                : 0,
          ),
        );
      case dashboard:
        final args = settings.arguments as Map<String, dynamic>;
        final propertyId = args['propertyId'] as int;
        final propertyName = args['propertyName'] as String;
        return MaterialPageRoute(
          builder: (_) => BlocProvider(
            create: (_) =>
                AppBindings.createDashboardCubit()..loadDashboard(propertyId),
            child: DashboardPage(
              propertyId: propertyId,
              propertyName: propertyName,
            ),
          ),
          settings: settings,
        );
      case modules:
        return MaterialPageRoute(builder: (_) => const ModulesPage());
      case moduleStore:
        return MaterialPageRoute(builder: (_) => const ModuleStorePage());
      default:
        return MaterialPageRoute(builder: (_) => const WelcomePage());
    }
  }
}

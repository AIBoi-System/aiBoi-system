import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'core/theme/app_colors.dart';
import 'features/auth/presentation/cubits/login_cubit.dart';
import 'features/auth/presentation/pages/login_page.dart';

void main() {
  runApp(const AiBoiApp());
}

class AiBoiApp extends StatelessWidget {
  const AiBoiApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Ai Boi',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: AppColors.primaryButton),
        useMaterial3: true,
        fontFamily: 'Poppins',
      ),
      home: BlocProvider(
        create: (context) => LoginCubit(),
        child: const LoginPage(),
      ),
    );
  }
}
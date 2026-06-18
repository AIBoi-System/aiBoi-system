import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:flutter/material.dart';

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
      initialRoute: AppRouter.welcome,
      onGenerateRoute: AppRouter.onGenerateRoute,
    );
  }
}


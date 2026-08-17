import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/theme/theme_cubit.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class AiBoiApp extends StatelessWidget {
  const AiBoiApp({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => ThemeCubit(),
      child: BlocBuilder<ThemeCubit, ThemeMode>(
        builder: (context, themeMode) {
          return MaterialApp(
            title: 'AgroFence',
            debugShowCheckedModeBanner: false,
            themeMode: themeMode,
            theme: ThemeData(
              colorScheme: ColorScheme.fromSeed(
                seedColor: AppColors.primaryButton,
                primary: AppColors.primaryButton,
                surface: Colors.white,
              ),
              useMaterial3: true,
              fontFamily: 'Poppins',
            ),
            darkTheme: ThemeData(
              colorScheme: ColorScheme.fromSeed(
                seedColor: AppColors.primaryButton,
                brightness: Brightness.dark,
                primary: AppColors.primaryButton,
                surface: const Color(0xFF121212),
              ),
              scaffoldBackgroundColor: const Color(0xFF121212),
              appBarTheme: const AppBarTheme(
                backgroundColor: Color(0xFF121212),
                surfaceTintColor: Color(0xFF121212),
                iconTheme: IconThemeData(color: Colors.white),
              ),
              useMaterial3: true,
              fontFamily: 'Poppins',
            ),
            initialRoute: AppRouter.welcome,
            onGenerateRoute: AppRouter.onGenerateRoute,
            builder: (context, child) {
              final isDark = themeMode == ThemeMode.dark;
              return ColoredBox(
                color: isDark ? Colors.black : const Color(0xFFF1F1F7),
                child: Center(
                  child: ConstrainedBox(
                    constraints: const BoxConstraints(maxWidth: 412),
                    child: SizedBox.expand(child: child),
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}

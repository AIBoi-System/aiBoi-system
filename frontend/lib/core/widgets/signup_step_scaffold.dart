import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/step_progress_bar.dart';
import 'package:flutter/material.dart';

class SignupStepScaffold extends StatelessWidget {
  final String title;
  final int currentStep;
  final int totalSteps;
  final Widget child;
  final Widget? bottom;

  const SignupStepScaffold({
    super.key,
    required this.title,
    required this.currentStep,
    this.totalSteps = 3,
    required this.child,
    this.bottom,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          '$title $currentStep / $totalSteps',
          style: const TextStyle(
            color: Colors.black,
            fontSize: 16,
            fontWeight: FontWeight.w600,
            fontFamily: 'Poppins',
          ),
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24),
              child: StepProgressBar(
                currentStep: currentStep,
                totalSteps: totalSteps,
              ),
            ),
            const SizedBox(height: 24),
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 24),
                child: child,
              ),
            ),
            if (bottom != null)
              Padding(
                padding: const EdgeInsets.fromLTRB(24, 8, 24, 24),
                child: bottom!,
              ),
          ],
        ),
      ),
    );
  }
}

class SignupSimpleScaffold extends StatelessWidget {
  final String title;
  final Widget child;
  final Widget? bottom;
  final String? subtitle;

  const SignupSimpleScaffold({
    super.key,
    required this.title,
    this.subtitle,
    required this.child,
    this.bottom,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          title,
          style: const TextStyle(
            color: Colors.black,
            fontSize: 16,
            fontWeight: FontWeight.w600,
            fontFamily: 'Poppins',
          ),
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (subtitle != null)
              Padding(
                padding: const EdgeInsets.fromLTRB(24, 8, 24, 16),
                child: Text(
                  subtitle!,
                  style: const TextStyle(
                    color: AppColors.textSecondary,
                    fontSize: 14,
                    height: 1.4,
                    fontFamily: 'Poppins',
                  ),
                ),
              ),
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 24),
                child: child,
              ),
            ),
            if (bottom != null)
              Padding(
                padding: const EdgeInsets.fromLTRB(24, 8, 24, 24),
                child: bottom!,
              ),
          ],
        ),
      ),
    );
  }
}

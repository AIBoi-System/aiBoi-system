import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:flutter/material.dart';

class AnimalStepHeader extends StatelessWidget {
  const AnimalStepHeader({
    super.key,
    required this.currentStep,
    this.totalSteps = 5,
    this.labels = const [
      'Identificação',
      'Localização',
      'Pesagem',
      'Genealogia',
      'Resumo',
    ],
  });

  final int currentStep;
  final int totalSteps;
  final List<String> labels;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          children: List.generate(totalSteps * 2 - 1, (index) {
            if (index.isOdd) {
              final leftStep = index ~/ 2 + 1;
              return Expanded(
                child: Container(
                  height: 2,
                  color: leftStep < currentStep
                      ? AppColors.primaryButton
                      : Colors.grey.shade300,
                ),
              );
            }

            final step = index ~/ 2 + 1;
            final done = step < currentStep;
            final active = step == currentStep;
            return Expanded(
              child: Container(
                alignment: Alignment.center,
                child: Container(
                  width: 28,
                  height: 28,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: done || active
                        ? AppColors.primaryButton
                        : Colors.grey.shade300,
                  ),
                  child: Center(
                    child: done
                        ? const Icon(Icons.check, color: Colors.white, size: 16)
                        : Text(
                            '$step',
                            style: TextStyle(
                              color: active ? Colors.white : Colors.grey.shade600,
                              fontWeight: FontWeight.bold,
                              fontSize: 12,
                            ),
                          ),
                  ),
                ),
              ),
            );
          }),
        ),
        const SizedBox(height: 8),
        Row(
          children: List.generate(totalSteps, (index) {
            final label = labels[index];
            return Expanded(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 2),
                child: Text(
                  label,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 10,
                    fontWeight: index + 1 == currentStep ? FontWeight.w600 : FontWeight.w500,
                    color: index + 1 == currentStep
                        ? AppColors.primaryButton
                        : Colors.grey.shade600,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            );
          }),
        ),
      ],
    );
  }
}


import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:flutter/material.dart';

class PrimaryButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final Color backgroundColor;
  final Color textColor;
  final double borderRadius;
  final double? width;
  final double height;
  final bool isLoading;
  final Widget? leading;

  const PrimaryButton({
    super.key,
    required this.text,
    required this.onPressed,
    this.backgroundColor = AppColors.primaryButton,
    this.textColor = Colors.white,
    this.borderRadius = 12.0,
    this.width,
    this.height = 60.0,
    this.isLoading = false,
    this.leading,
  });

  @override
  Widget build(BuildContext context) {
    final enabled = onPressed != null && !isLoading;
    final usesPrimaryPalette = backgroundColor == AppColors.primaryButton;

    return DecoratedBox(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(borderRadius),
        boxShadow: enabled && usesPrimaryPalette
            ? const [
                BoxShadow(
                  color: Color(0x291C6153),
                  blurRadius: 12,
                  offset: Offset(0, 12),
                  spreadRadius: -8,
                ),
              ]
            : const [],
      ),
      child: SizedBox(
        width: width ?? double.infinity,
        height: height,
        child: ElevatedButton(
          onPressed: enabled ? onPressed : null,
          style: ButtonStyle(
            elevation: const WidgetStatePropertyAll(0),
            padding: const WidgetStatePropertyAll(
              EdgeInsets.symmetric(horizontal: 16),
            ),
            foregroundColor: WidgetStatePropertyAll(textColor),
            backgroundColor: WidgetStateProperty.resolveWith((states) {
              if (states.contains(WidgetState.disabled)) {
                return usesPrimaryPalette
                    ? AppColors.buttonDisabled
                    : backgroundColor.withValues(alpha: 0.49);
              }
              if (states.contains(WidgetState.hovered) && usesPrimaryPalette) {
                return AppColors.primaryButtonHover;
              }
              return backgroundColor;
            }),
            overlayColor: WidgetStatePropertyAll(
              Colors.white.withValues(alpha: 0.08),
            ),
            shape: WidgetStatePropertyAll(
              RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(borderRadius),
              ),
            ),
            textStyle: const WidgetStatePropertyAll(
              TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
                fontFamily: 'Roboto',
                height: 1.6,
              ),
            ),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            mainAxisSize: MainAxisSize.min,
            children: [
              if (isLoading)
                const SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    color: Colors.white,
                  ),
                )
              else if (leading != null)
                SizedBox(width: 24, height: 24, child: leading),
              if (isLoading || leading != null) const SizedBox(width: 10),
              Text(text),
            ],
          ),
        ),
      ),
    );
  }

  static double heightFor(BuildContext context) => 60.0;
}

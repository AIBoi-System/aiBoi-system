import 'package:ai_boi/core/widgets/auth_method_scaffold.dart';
import 'package:ai_boi/core/widgets/labeled_text_field.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('primary action follows the 60px Figma button height', (
    tester,
  ) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: PrimaryButton(text: 'Continuar', onPressed: () {}),
        ),
      ),
    );

    expect(tester.getSize(find.byType(ElevatedButton)).height, 60);
  });

  testWidgets('auth method screen exposes email, Apple and Google actions', (
    tester,
  ) async {
    await tester.pumpWidget(
      MaterialApp(
        home: AuthMethodScaffold(
          title: 'Acesse sua conta',
          subtitle: 'Escolha como entrar.',
          onEmail: () {},
          onGoogle: () {},
          onApple: () {},
        ),
      ),
    );

    expect(find.text('Continue com e-mail'), findsOneWidget);
    expect(find.text('Continue com Apple'), findsOneWidget);
    expect(find.text('Continue com Google'), findsOneWidget);
    for (final element in find.byType(OutlinedButton).evaluate()) {
      expect(tester.getSize(find.byWidget(element.widget)).height, 60);
    }
  });

  testWidgets('labeled input keeps the 60px minimum control height', (
    tester,
  ) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: LabeledTextField(label: 'E-mail', hintText: 'seu@email.com'),
        ),
      ),
    );

    expect(tester.getSize(find.byType(TextFormField)).height, 60);
  });
}

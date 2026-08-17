import 'package:ai_boi/core/di/app_bindings.dart';
import 'package:ai_boi/features/activities/presentation/pages/activities_page.dart';
import 'package:ai_boi/features/profile/presentation/pages/profile_page.dart';
import 'package:ai_boi/features/settings/presentation/pages/settings_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  Widget app(Widget child) => MaterialApp(
    theme: ThemeData(useMaterial3: true, fontFamily: 'Poppins'),
    home: child,
  );

  testWidgets('configurações segue seções e alterna preferências', (
    tester,
  ) async {
    await tester.pumpWidget(app(const SettingsPage()));

    expect(find.text('Configurações'), findsOneWidget);
    expect(find.text('Notificações'), findsOneWidget);
    expect(find.text('Preferências'), findsOneWidget);
    final switches = find.byType(Switch);
    expect(switches, findsWidgets);
    expect(tester.widget<Switch>(switches.at(0)).value, isTrue);
    await tester.tap(switches.at(0));
    await tester.pump();
    expect(tester.widget<Switch>(switches.at(0)).value, isFalse);
    await tester.scrollUntilVisible(find.text('Conta e Segurança'), 350);
    expect(find.text('Conta e Segurança'), findsOneWidget);
  });

  testWidgets('perfil expõe as quatro abas do Figma', (tester) async {
    await tester.pumpWidget(app(const ProfilePage()));

    expect(find.text('Minha Conta'), findsOneWidget);
    expect(find.text('Notificações'), findsOneWidget);
    expect(find.text('Assinatura'), findsOneWidget);
    expect(find.text('Configurações'), findsOneWidget);

    await tester.tap(find.text('Assinatura'));
    await tester.pumpAndSettle();
    expect(find.text('AgroFence Pro'), findsOneWidget);
    expect(find.text('Fazer Upgrade de Plano'), findsOneWidget);

    await tester.tap(find.text('Configurações'));
    await tester.pumpAndSettle();
    expect(find.text('Tema Escuro (Dark Mode)'), findsOneWidget);
    expect(find.text('Sobre o App'), findsOneWidget);
  });

  testWidgets('atividades preserva os sete grupos do fluxo', (tester) async {
    await tester.pumpWidget(
      app(
        ActivitiesPage(
          propertyId: 1,
          propertyName: 'Sabiá Dourado',
          operations: AppBindings.operations(),
        ),
      ),
    );

    expect(find.text('Manejo'), findsOneWidget);
    expect(find.text('Reprodução'), findsOneWidget);
    expect(find.text('Sanidade'), findsOneWidget);
    expect(find.text('Pesagem'), findsOneWidget);
    await tester.drag(find.byType(ListView).first, const Offset(0, -500));
    await tester.pumpAndSettle();
    expect(find.text('Financeiro'), findsWidgets);
    await tester.drag(find.byType(ListView).first, const Offset(0, -600));
    await tester.pumpAndSettle();
    expect(find.text('Pastagem'), findsOneWidget);
    expect(find.text('Cercas Virtuais'), findsOneWidget);
  });
}

import 'package:ai_boi/core/di/app_bindings.dart';
import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/agrofence_shell.dart';
import 'package:flutter/material.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key, this.initialTab = 0});
  final int initialTab;
  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  late int _tab = widget.initialTab.clamp(0, 3);
  bool sound = true;
  bool push = true;
  bool email = false;
  bool dark = false;

  @override
  Widget build(BuildContext context) => Scaffold(
    backgroundColor: Colors.white,
    body: SafeArea(
      child: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(24, 20, 24, 10),
            child: Row(
              children: [
                IconButton.outlined(
                  onPressed: () => Navigator.maybePop(context),
                  icon: const Icon(
                    Icons.arrow_back,
                    color: AppColors.figmaPrimary,
                  ),
                  style: IconButton.styleFrom(
                    side: const BorderSide(color: AppColors.figmaBorder),
                  ),
                ),
                const Expanded(
                  child: Text(
                    'Meu Perfil',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      color: AppColors.figmaPrimary,
                      fontSize: 20,
                      fontWeight: FontWeight.w800,
                      fontFamily: 'Poppins',
                    ),
                  ),
                ),
                IconButton.outlined(
                  onPressed: () {},
                  icon: const Icon(
                    Icons.qr_code_scanner_rounded,
                    color: AppColors.figmaPrimary,
                  ),
                  style: IconButton.styleFrom(
                    side: const BorderSide(color: AppColors.figmaBorder),
                  ),
                ),
              ],
            ),
          ),
          const CircleAvatar(
            radius: 38,
            backgroundColor: AppColors.figmaSoftGreen,
            child: Icon(
              Icons.person,
              size: 36,
              color: AppColors.figmaPrimary700,
            ),
          ),
          const SizedBox(height: 14),
          const Text(
            'João Pereira',
            style: TextStyle(
              color: AppColors.figmaPrimary,
              fontSize: 18,
              fontWeight: FontWeight.w800,
              fontFamily: 'Poppins',
            ),
          ),
          const SizedBox(height: 3),
          const Text(
            'Fazenda Boa Esperança · Itacarambi, MG',
            style: TextStyle(color: AppColors.figmaMuted, fontSize: 12),
          ),
          const SizedBox(height: 20),
          SizedBox(
            height: 42,
            child: ListView.separated(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 24),
              itemCount: 4,
              separatorBuilder: (_, _) => const SizedBox(width: 8),
              itemBuilder: (_, index) => ChoiceChip(
                label: Text(
                  const [
                    'Minha Conta',
                    'Notificações',
                    'Assinatura',
                    'Configurações',
                  ][index],
                ),
                selected: _tab == index,
                onSelected: (_) => setState(() => _tab = index),
                selectedColor: AppColors.figmaSecondary,
                backgroundColor: Colors.white,
                side: BorderSide(
                  color: _tab == index
                      ? AppColors.figmaSecondary
                      : AppColors.figmaBorder,
                ),
                labelStyle: TextStyle(
                  color: _tab == index ? Colors.white : AppColors.figmaMuted,
                  fontWeight: FontWeight.w600,
                ),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(22),
                ),
                showCheckmark: false,
              ),
            ),
          ),
          const SizedBox(height: 14),
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.fromLTRB(24, 0, 24, 30),
              child: _content(context),
            ),
          ),
        ],
      ),
    ),
  );

  Widget _content(BuildContext context) {
    switch (_tab) {
      case 1:
        return AgroFenceCard(
          child: Column(
            children: const [
              _Notification(
                icon: Icons.warning,
                tint: Color(0xFFFFEDD5),
                color: Color(0xFFEA580C),
                title: 'Bateria Crítica',
                body: 'Coleira #C118 (Lote 03) está com apenas 15% de bateria.',
                time: 'Agora',
              ),
              _Notification(
                icon: Icons.grid_on_rounded,
                tint: Color(0xFFDBEAFE),
                color: Color(0xFF2563EB),
                title: 'Limite Atingido',
                body: 'Animal #842 aproximou-se da cerca virtual Leste.',
                time: '1h',
              ),
              _Notification(
                icon: Icons.check_circle,
                tint: Color(0xFFDCFCE7),
                color: Color(0xFF16A34A),
                title: 'Fatura Paga',
                body: 'O pagamento do plano AgroFence Pro foi confirmado.',
                time: 'Ontem',
                last: true,
              ),
            ],
          ),
        );
      case 2:
        return Column(
          children: [
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppColors.figmaPrimary700,
                borderRadius: BorderRadius.circular(16),
                boxShadow: [
                  BoxShadow(
                    color: AppColors.figmaPrimary.withValues(alpha: .2),
                    blurRadius: 15,
                    offset: const Offset(0, 8),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 9,
                      vertical: 4,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.white.withValues(alpha: .18),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: const Text(
                      'PLANO ATIVO',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 9,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                  const SizedBox(height: 13),
                  const Text(
                    'AgroFence Pro',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 19,
                      fontWeight: FontWeight.w800,
                      fontFamily: 'Poppins',
                    ),
                  ),
                  const SizedBox(height: 5),
                  const Text(
                    'Até 1.500 animais monitorados em tempo real.\nSuporte prioritário 24/7.',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 12,
                      height: 1.35,
                    ),
                  ),
                  const SizedBox(height: 14),
                  SizedBox(
                    width: double.infinity,
                    child: FilledButton(
                      onPressed: () {},
                      style: FilledButton.styleFrom(
                        backgroundColor: Colors.white,
                        foregroundColor: AppColors.figmaPrimary,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(11),
                        ),
                      ),
                      child: const Text(
                        'Fazer Upgrade de Plano',
                        style: TextStyle(fontWeight: FontWeight.w700),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),
            const AgroFenceCard(
              child: Column(
                children: [
                  _ProfileLink(
                    icon: Icons.credit_card,
                    tint: Color(0xFFCCFBF1),
                    color: Color(0xFF0F766E),
                    title: 'Método de Pagamento',
                    subtitle: 'Mastercard final 4821',
                  ),
                  _ProfileLink(
                    icon: Icons.receipt_long,
                    tint: Color(0xFFF3E8FF),
                    color: Color(0xFF9333EA),
                    title: 'Histórico de Faturas',
                    subtitle: 'Visualize recibos anteriores',
                    last: true,
                  ),
                ],
              ),
            ),
          ],
        );
      case 3:
        return Column(
          children: [
            AgroFenceCard(
              child: Column(
                children: [
                  _ProfileToggle(
                    title: 'Alertas Sonoros',
                    subtitle: 'Tocar som no aplicativo',
                    value: sound,
                    onChanged: (v) => setState(() => sound = v),
                  ),
                  _ProfileToggle(
                    title: 'Notificações Push',
                    subtitle: 'Alertas em tempo real na tela',
                    value: push,
                    onChanged: (v) => setState(() => push = v),
                  ),
                  _ProfileToggle(
                    title: 'Resumo por E-mail',
                    subtitle: 'Relatório diário do rebanho',
                    value: email,
                    onChanged: (v) => setState(() => email = v),
                  ),
                  _ProfileToggle(
                    title: 'Tema Escuro (Dark Mode)',
                    subtitle: 'Adaptar às configurações do sistema',
                    value: dark,
                    onChanged: (v) => setState(() => dark = v),
                    last: true,
                  ),
                ],
              ),
            ),
            const SizedBox(height: 14),
            const AgroFenceCard(
              child: Column(
                children: [
                  _ProfileLink(
                    icon: Icons.help,
                    tint: Color(0xFFF3F4F6),
                    color: Color(0xFF4B5563),
                    title: 'Central de Ajuda',
                    subtitle: 'Manuais e tutoriais de uso',
                  ),
                  _ProfileLink(
                    icon: Icons.info,
                    tint: Color(0xFFF3F4F6),
                    color: Color(0xFF4B5563),
                    title: 'Sobre o App',
                    subtitle: 'Versão 2.1.4 (Build 409)',
                    last: true,
                  ),
                ],
              ),
            ),
          ],
        );
      default:
        return Column(
          children: [
            AgroFenceCard(
              child: Column(
                children: [
                  const _ProfileLink(
                    icon: Icons.badge,
                    tint: Color(0xFFF3E8FF),
                    color: Color(0xFF9333EA),
                    title: 'Dados Pessoais',
                    subtitle: 'Nome, e-mail e documento',
                  ),
                  _ProfileLink(
                    icon: Icons.landscape,
                    tint: AppColors.figmaSoftGreen,
                    color: AppColors.figmaSecondary,
                    title: 'Propriedades',
                    subtitle: 'Gerenciar minhas fazendas',
                    onTap: () =>
                        Navigator.pushNamed(context, AppRouter.properties),
                  ),
                  const _ProfileLink(
                    icon: Icons.lock_reset,
                    tint: Color(0xFFF3F4F6),
                    color: Color(0xFF4B5563),
                    title: 'Segurança',
                    subtitle: 'Alteração de senha e PIN',
                    last: true,
                  ),
                ],
              ),
            ),
            const SizedBox(height: 14),
            AgroFenceCard(
              child: _ProfileLink(
                icon: Icons.logout,
                tint: const Color(0xFFFEE2E2),
                color: Colors.red,
                title: 'Sair da conta',
                danger: true,
                last: true,
                onTap: () => _logout(context),
              ),
            ),
          ],
        );
    }
  }

  Future<void> _logout(BuildContext context) async {
    try {
      await AppBindings.authRepository.logout();
    } finally {
      if (context.mounted) {
        Navigator.pushNamedAndRemoveUntil(
          context,
          AppRouter.welcome,
          (_) => false,
        );
      }
    }
  }
}

class _ProfileLink extends StatelessWidget {
  const _ProfileLink({
    required this.icon,
    required this.tint,
    required this.color,
    required this.title,
    this.subtitle,
    this.onTap,
    this.last = false,
    this.danger = false,
  });
  final IconData icon;
  final Color tint;
  final Color color;
  final String title;
  final String? subtitle;
  final VoidCallback? onTap;
  final bool last;
  final bool danger;
  @override
  Widget build(BuildContext context) => InkWell(
    onTap: onTap,
    child: Container(
      padding: const EdgeInsets.symmetric(vertical: 13, horizontal: 4),
      decoration: BoxDecoration(
        border: last
            ? null
            : const Border(bottom: BorderSide(color: AppColors.figmaBorder)),
      ),
      child: Row(
        children: [
          Container(
            width: 38,
            height: 38,
            decoration: BoxDecoration(
              color: tint,
              borderRadius: BorderRadius.circular(11),
            ),
            child: Icon(icon, color: color, size: 19),
          ),
          const SizedBox(width: 13),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    color: danger ? Colors.red : AppColors.figmaText,
                    fontSize: 13,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                if (subtitle != null)
                  Text(
                    subtitle!,
                    style: const TextStyle(
                      color: AppColors.figmaMuted,
                      fontSize: 11,
                    ),
                  ),
              ],
            ),
          ),
          if (!danger)
            const Icon(Icons.chevron_right, size: 19, color: Color(0xFF9CA3AF)),
        ],
      ),
    ),
  );
}

class _Notification extends StatelessWidget {
  const _Notification({
    required this.icon,
    required this.tint,
    required this.color,
    required this.title,
    required this.body,
    required this.time,
    this.last = false,
  });
  final IconData icon;
  final Color tint;
  final Color color;
  final String title;
  final String body;
  final String time;
  final bool last;
  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(vertical: 10),
    decoration: BoxDecoration(
      border: last
          ? null
          : const Border(bottom: BorderSide(color: AppColors.figmaBorder)),
    ),
    child: Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: 38,
          height: 38,
          decoration: BoxDecoration(
            color: tint,
            borderRadius: BorderRadius.circular(10),
          ),
          child: Icon(icon, color: color, size: 18),
        ),
        const SizedBox(width: 11),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: const TextStyle(
                  color: AppColors.figmaText,
                  fontWeight: FontWeight.w700,
                  fontSize: 13,
                ),
              ),
              Text(
                body,
                style: const TextStyle(
                  color: AppColors.figmaMuted,
                  fontSize: 11,
                  height: 1.25,
                ),
              ),
            ],
          ),
        ),
        Text(
          time,
          style: const TextStyle(color: Color(0xFF9CA3AF), fontSize: 10),
        ),
      ],
    ),
  );
}

class _ProfileToggle extends StatelessWidget {
  const _ProfileToggle({
    required this.title,
    required this.subtitle,
    required this.value,
    required this.onChanged,
    this.last = false,
  });
  final String title;
  final String subtitle;
  final bool value;
  final ValueChanged<bool> onChanged;
  final bool last;
  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 4),
    decoration: BoxDecoration(
      border: last
          ? null
          : const Border(bottom: BorderSide(color: AppColors.figmaBorder)),
    ),
    child: Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: const TextStyle(
                  color: AppColors.figmaText,
                  fontSize: 13,
                  fontWeight: FontWeight.w700,
                ),
              ),
              Text(
                subtitle,
                style: const TextStyle(
                  color: AppColors.figmaMuted,
                  fontSize: 11,
                ),
              ),
            ],
          ),
        ),
        Switch(
          value: value,
          onChanged: onChanged,
          activeTrackColor: AppColors.figmaSecondary,
        ),
      ],
    ),
  );
}

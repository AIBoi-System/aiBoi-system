import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/agrofence_shell.dart';
import 'package:ai_boi/core/theme/theme_cubit.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter/material.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});
  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  bool sound = true;
  bool push = true;
  bool email = false;

  @override
  void initState() {
    super.initState();
    _loadPreferences();
  }

  Future<void> _loadPreferences() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      sound = prefs.getBool('pref_sound') ?? true;
      push = prefs.getBool('pref_push') ?? true;
      email = prefs.getBool('pref_email') ?? false;
    });
  }

  Future<void> _savePreference(String key, bool value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(key, value);
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    bool isDark = theme.brightness == Brightness.dark;
    try {
      final themeCubit = BlocProvider.of<ThemeCubit>(context, listen: true);
      isDark = themeCubit.state == ThemeMode.dark;
    } catch (_) {}
    final isDarkMode = isDark;

    return Scaffold(
      backgroundColor: theme.scaffoldBackgroundColor,
      appBar: AppBar(
        backgroundColor: theme.scaffoldBackgroundColor,
        surfaceTintColor: Colors.transparent,
        leading: Padding(
          padding: const EdgeInsets.all(7),
          child: IconButton.filledTonal(
            onPressed: () => Navigator.maybePop(context),
            icon: Icon(Icons.arrow_back, color: isDarkMode ? Colors.white : AppColors.figmaPrimary),
            style: IconButton.styleFrom(
              backgroundColor: isDarkMode ? const Color(0xFF2C2C2C) : Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10),
                side: BorderSide(color: isDarkMode ? Colors.transparent : AppColors.figmaBorder),
              ),
            ),
          ),
        ),
        title: Text(
          'Configurações',
          style: TextStyle(
            color: isDarkMode ? Colors.white : AppColors.figmaPrimary,
            fontSize: 20,
            fontWeight: FontWeight.w800,
            fontFamily: 'Poppins',
          ),
        ),
      centerTitle: true,
    ),
    body: SafeArea(
      child: ListView(
        padding: const EdgeInsets.fromLTRB(24, 18, 24, 30),
        children: [
          const _SectionTitle(icon: Icons.notifications, title: 'Notificações'),
          AgroFenceCard(
            child: Column(
              children: [
                _ToggleRow(
                  title: 'Alertas Sonoros',
                  subtitle: 'Tocar som no aplicativo',
                  value: sound,
                  onChanged: (v) {
                    setState(() => sound = v);
                    _savePreference('pref_sound', v);
                  },
                ),
                _ToggleRow(
                  title: 'Notificações Push',
                  subtitle: 'Alertas em tempo real na tela',
                  value: push,
                  onChanged: (v) {
                    setState(() => push = v);
                    _savePreference('pref_push', v);
                  },
                ),
                _ToggleRow(
                  title: 'Resumo por E-mail',
                  subtitle: 'Relatório diário do rebanho',
                  value: email,
                  onChanged: (v) {
                    setState(() => email = v);
                    _savePreference('pref_email', v);
                  },
                  last: true,
                ),
              ],
            ),
          ),
          const SizedBox(height: 25),
          const _SectionTitle(
            icon: Icons.tune_rounded,
            title: 'Preferências',
            color: Color(0xFF9333EA),
          ),
          AgroFenceCard(
            child: Column(
              children: [
                _ToggleRow(
                  title: 'Tema Escuro (Dark Mode)',
                  subtitle: 'Adaptar às configurações do sistema',
                  value: isDark,
                  onChanged: (v) {
                    context.read<ThemeCubit>().toggleTheme(v);
                  },
                ),
                const _LinkRow(
                  icon: Icons.language,
                  title: 'Idioma',
                  subtitle: 'Português (Brasil)',
                  tint: Color(0xFFF3E8FF),
                  iconColor: Color(0xFF9333EA),
                ),
                _LinkRow(
                  icon: Icons.landscape_rounded,
                  title: 'Fazendas',
                  subtitle: 'Gerenciar propriedades vinculadas',
                  tint: AppColors.figmaSoftGreen,
                  iconColor: AppColors.figmaSecondary,
                  onTap: () =>
                      Navigator.pushNamed(context, AppRouter.properties),
                  last: true,
                ),
              ],
            ),
          ),
          const SizedBox(height: 25),
          const _SectionTitle(
            icon: Icons.shield_outlined,
            title: 'Conta e Segurança',
            color: Color(0xFF4B5563),
          ),
          const AgroFenceCard(
            child: Column(
              children: [
                _LinkRow(
                  icon: Icons.lock_reset_rounded,
                  title: 'Alterar Senha e PIN',
                  tint: Color(0xFFF3F4F6),
                  iconColor: Color(0xFF4B5563),
                ),
                _LinkRow(
                  icon: Icons.help_rounded,
                  title: 'Central de Ajuda',
                  subtitle: 'Manuais e tutoriais de uso',
                  tint: Color(0xFFF3F4F6),
                  iconColor: Color(0xFF4B5563),
                  last: true,
                ),
              ],
            ),
          ),
        ],
      ),
    ),
  );
  }
}

class _SectionTitle extends StatelessWidget {
  const _SectionTitle({
    required this.icon,
    required this.title,
    this.color = AppColors.figmaSecondary,
  });
  final IconData icon;
  final String title;
  final Color color;
  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 12, left: 2),
    child: Row(
      children: [
        Icon(icon, color: color, size: 18),
        const SizedBox(width: 9),
        Text(
          title,
          style: TextStyle(
            color: Theme.of(context).brightness == Brightness.dark ? Colors.white : AppColors.figmaPrimary,
            fontSize: 16,
            fontWeight: FontWeight.w800,
            fontFamily: 'Poppins',
          ),
        ),
      ],
    ),
  );
}

class _ToggleRow extends StatelessWidget {
  const _ToggleRow({
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
    padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 4),
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
                style: TextStyle(
                  color: Theme.of(context).brightness == Brightness.dark ? Colors.white : AppColors.figmaText,
                  fontWeight: FontWeight.w700,
                  fontSize: 14,
                ),
              ),
              Text(
                subtitle,
                style: TextStyle(
                  color: Theme.of(context).brightness == Brightness.dark ? Colors.white70 : AppColors.figmaMuted,
                  fontSize: 12,
                ),
              ),
            ],
          ),
        ),
        Switch(
          value: value,
          onChanged: onChanged,
          activeTrackColor: AppColors.figmaSecondary,
          inactiveTrackColor: const Color(0xFFE5E7EB),
          inactiveThumbColor: Colors.white,
        ),
      ],
    ),
  );
}

class _LinkRow extends StatelessWidget {
  const _LinkRow({
    required this.icon,
    required this.title,
    required this.tint,
    required this.iconColor,
    this.subtitle,
    this.onTap,
    this.last = false,
  });
  final IconData icon;
  final String title;
  final String? subtitle;
  final Color tint;
  final Color iconColor;
  final VoidCallback? onTap;
  final bool last;
  @override
  Widget build(BuildContext context) => InkWell(
    onTap: onTap,
    child: Container(
      padding: const EdgeInsets.symmetric(vertical: 11, horizontal: 4),
      decoration: BoxDecoration(
        border: last
            ? null
            : const Border(bottom: BorderSide(color: AppColors.figmaBorder)),
      ),
      child: Row(
        children: [
          Container(
            width: 42,
            height: 42,
            decoration: BoxDecoration(
              color: tint,
              borderRadius: BorderRadius.circular(11),
            ),
            child: Icon(icon, color: iconColor, size: 20),
          ),
          const SizedBox(width: 13),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    color: Theme.of(context).brightness == Brightness.dark ? Colors.white : AppColors.figmaText,
                    fontWeight: FontWeight.w700,
                    fontSize: 14,
                  ),
                ),
                if (subtitle != null)
                  Text(
                    subtitle!,
                    style: TextStyle(
                      color: Theme.of(context).brightness == Brightness.dark ? Colors.white70 : AppColors.figmaMuted,
                      fontSize: 12,
                    ),
                  ),
              ],
            ),
          ),
          const Icon(Icons.chevron_right, color: Color(0xFF9CA3AF), size: 20),
        ],
      ),
    ),
  );
}

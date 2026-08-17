import 'package:ai_boi/core/di/app_bindings.dart';
import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';
import 'package:flutter/material.dart';

Future<RegisteredProperty?> showPropertySelectorSheet(
  BuildContext context, {
  required String currentPropertyName,
  ValueChanged<RegisteredProperty>? onSelected,
}) {
  return showModalBottomSheet<RegisteredProperty>(
    context: context,
    isScrollControlled: true,
    backgroundColor: Colors.transparent,
    builder: (ctx) => PropertySelectorSheet(
      currentPropertyName: currentPropertyName,
      onSelected: onSelected,
    ),
  );
}

class PropertySelectorSheet extends StatefulWidget {
  const PropertySelectorSheet({
    super.key,
    required this.currentPropertyName,
    this.onSelected,
  });

  final String currentPropertyName;
  final ValueChanged<RegisteredProperty>? onSelected;

  @override
  State<PropertySelectorSheet> createState() => _PropertySelectorSheetState();
}

class _PropertySelectorSheetState extends State<PropertySelectorSheet> {
  late Future<List<RegisteredProperty>> _propertiesFuture;

  @override
  void initState() {
    super.initState();
    _propertiesFuture = AppBindings.propertyRepository().listProperties();
  }

  void _reload() {
    setState(() {
      _propertiesFuture = AppBindings.propertyRepository().listProperties();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      padding: EdgeInsets.only(
        bottom: MediaQuery.of(context).viewInsets.bottom + 24,
      ),
      child: SafeArea(
        top: false,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const SizedBox(height: 12),
            Center(
              child: Container(
                width: 44,
                height: 4,
                decoration: BoxDecoration(
                  color: const Color(0xFFE5E7EB),
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 16, 20, 12),
              child: Row(
                children: [
                  Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: AppColors.figmaSoftGreen,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: const Icon(
                      Icons.landscape_rounded,
                      color: AppColors.figmaSecondary,
                      size: 22,
                    ),
                  ),
                  const SizedBox(width: 12),
                  const Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Trocar de Fazenda',
                          style: TextStyle(
                            fontSize: 17,
                            fontWeight: FontWeight.w800,
                            fontFamily: 'Poppins',
                            color: AppColors.figmaPrimary,
                          ),
                        ),
                        SizedBox(height: 2),
                        Text(
                          'Selecione a propriedade que deseja gerenciar',
                          style: TextStyle(
                            fontSize: 12,
                            color: AppColors.figmaMuted,
                          ),
                        ),
                      ],
                    ),
                  ),
                  IconButton(
                    onPressed: () => Navigator.pop(context),
                    icon: const Icon(Icons.close_rounded),
                    color: AppColors.figmaMuted,
                  ),
                ],
              ),
            ),
            const Divider(height: 1, color: Color(0xFFF3F4F6)),
            ConstrainedBox(
              constraints: BoxConstraints(
                maxHeight: MediaQuery.of(context).size.height * 0.45,
              ),
              child: FutureBuilder<List<RegisteredProperty>>(
                future: _propertiesFuture,
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const Padding(
                      padding: EdgeInsets.symmetric(vertical: 36),
                      child: Center(child: CircularProgressIndicator()),
                    );
                  }
                  if (snapshot.hasError) {
                    return Padding(
                      padding: const EdgeInsets.all(24),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(
                            Icons.error_outline_rounded,
                            color: Colors.red,
                            size: 32,
                          ),
                          const SizedBox(height: 8),
                          const Text(
                            'Erro ao carregar propriedades',
                            style: TextStyle(
                              color: AppColors.figmaPrimary,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          TextButton(
                            onPressed: _reload,
                            child: const Text('Tentar novamente'),
                          ),
                        ],
                      ),
                    );
                  }

                  final properties = snapshot.data ?? const [];
                  if (properties.isEmpty) {
                    return Padding(
                      padding: const EdgeInsets.all(28),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(
                            Icons.nature_people_rounded,
                            size: 44,
                            color: AppColors.figmaMuted,
                          ),
                          const SizedBox(height: 12),
                          const Text(
                            'Nenhuma propriedade cadastrada',
                            style: TextStyle(
                              fontWeight: FontWeight.w700,
                              color: AppColors.figmaPrimary,
                              fontSize: 15,
                            ),
                          ),
                          const SizedBox(height: 4),
                          const Text(
                            'Cadastre uma nova fazenda para começar a gerenciar.',
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              color: AppColors.figmaMuted,
                              fontSize: 12,
                            ),
                          ),
                          const SizedBox(height: 16),
                          ElevatedButton.icon(
                            onPressed: () async {
                              Navigator.pop(context);
                              await Navigator.pushNamed(
                                context,
                                AppRouter.propertyCreate,
                              );
                            },
                            icon: const Icon(Icons.add, size: 18),
                            label: const Text('Cadastrar Nova Fazenda'),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: AppColors.figmaSecondary,
                              foregroundColor: Colors.white,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(10),
                              ),
                            ),
                          ),
                        ],
                      ),
                    );
                  }

                  return ListView.separated(
                    shrinkWrap: true,
                    padding: const EdgeInsets.symmetric(
                      horizontal: 18,
                      vertical: 12,
                    ),
                    itemCount: properties.length,
                    separatorBuilder: (_, _) => const SizedBox(height: 8),
                    itemBuilder: (context, index) {
                      final prop = properties[index];
                      final isCurrent =
                          prop.name.trim().toLowerCase() ==
                          widget.currentPropertyName.trim().toLowerCase();

                      return Material(
                        color: isCurrent
                            ? AppColors.figmaSoftGreen.withValues(alpha: .5)
                            : const Color(0xFFF9FAFB),
                        borderRadius: BorderRadius.circular(12),
                        child: InkWell(
                          onTap: () {
                            Navigator.pop(context, prop);
                            widget.onSelected?.call(prop);
                          },
                          borderRadius: BorderRadius.circular(12),
                          child: Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(
                                color: isCurrent
                                    ? AppColors.figmaSecondary
                                    : const Color(0xFFE5E7EB),
                                width: isCurrent ? 1.5 : 1,
                              ),
                            ),
                            child: Row(
                              children: [
                                Container(
                                  width: 40,
                                  height: 40,
                                  decoration: BoxDecoration(
                                    color: isCurrent
                                        ? AppColors.figmaSecondary
                                        : AppColors.figmaSoftGreen,
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                  child: Icon(
                                    Icons.landscape_rounded,
                                    color: isCurrent
                                        ? Colors.white
                                        : AppColors.figmaSecondary,
                                    size: 22,
                                  ),
                                ),
                                const SizedBox(width: 12),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        prop.name,
                                        style: TextStyle(
                                          fontWeight: FontWeight.w700,
                                          fontSize: 14,
                                          color: isCurrent
                                              ? AppColors.figmaSecondary
                                              : AppColors.figmaPrimary,
                                        ),
                                      ),
                                      const SizedBox(height: 2),
                                      Text(
                                        '${prop.cityState} · ${prop.hectares.toStringAsFixed(0)} ha · ${prop.purpose}',
                                        style: const TextStyle(
                                          color: AppColors.figmaMuted,
                                          fontSize: 11,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                                if (isCurrent)
                                  Container(
                                    padding: const EdgeInsets.symmetric(
                                      horizontal: 8,
                                      vertical: 4,
                                    ),
                                    decoration: BoxDecoration(
                                      color: AppColors.figmaSecondary,
                                      borderRadius: BorderRadius.circular(20),
                                    ),
                                    child: const Row(
                                      mainAxisSize: MainAxisSize.min,
                                      children: [
                                        Icon(
                                          Icons.check,
                                          color: Colors.white,
                                          size: 13,
                                        ),
                                        SizedBox(width: 4),
                                        Text(
                                          'Ativa',
                                          style: TextStyle(
                                            color: Colors.white,
                                            fontSize: 11,
                                            fontWeight: FontWeight.w700,
                                          ),
                                        ),
                                      ],
                                    ),
                                  )
                                else
                                  const Icon(
                                    Icons.chevron_right_rounded,
                                    color: Color(0xFF9CA3AF),
                                    size: 20,
                                  ),
                              ],
                            ),
                          ),
                        ),
                      );
                    },
                  );
                },
              ),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(18, 8, 18, 0),
              child: Row(
                children: [
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: () {
                        Navigator.pop(context);
                        Navigator.pushNamed(context, AppRouter.properties);
                      },
                      icon: const Icon(Icons.list_alt_rounded, size: 17),
                      label: const Text('Ver Todas'),
                      style: OutlinedButton.styleFrom(
                        foregroundColor: AppColors.figmaPrimary,
                        side: const BorderSide(color: Color(0xFFD1D5DB)),
                        padding: const EdgeInsets.symmetric(vertical: 12),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: ElevatedButton.icon(
                      onPressed: () async {
                        Navigator.pop(context);
                        final res = await Navigator.pushNamed(
                          context,
                          AppRouter.propertyCreate,
                        );
                        if (res == true && context.mounted) {
                          Navigator.pushReplacementNamed(
                            context,
                            AppRouter.properties,
                          );
                        }
                      },
                      icon: const Icon(Icons.add, size: 17),
                      label: const Text('Nova Fazenda'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.figmaPrimary700,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 12),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10),
                        ),
                      ),
                    ),
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

class AgroFenceTopBar extends StatelessWidget {
  const AgroFenceTopBar({
    super.key,
    required this.propertyName,
    this.onMenu,
    this.onNotifications,
    this.onPropertyTap,
    this.onPropertySelected,
  });

  final String propertyName;
  final VoidCallback? onMenu;
  final VoidCallback? onNotifications;
  final VoidCallback? onPropertyTap;
  final ValueChanged<RegisteredProperty>? onPropertySelected;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(24, 20, 24, 16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          _HeaderButton(icon: Icons.menu_rounded, onTap: onMenu),
          Material(
            color: Colors.white,
            borderRadius: BorderRadius.circular(10),
            child: InkWell(
              onTap: () {
                if (onPropertyTap != null) {
                  onPropertyTap!();
                } else {
                  showPropertySelectorSheet(
                    context,
                    currentPropertyName: propertyName,
                    onSelected: onPropertySelected,
                  );
                }
              },
              borderRadius: BorderRadius.circular(10),
              child: Container(
                constraints: const BoxConstraints(maxWidth: 205),
                padding: const EdgeInsets.fromLTRB(9, 7, 14, 7),
                decoration: _headerDecoration(),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      width: 34,
                      height: 34,
                      decoration: BoxDecoration(
                        color: AppColors.figmaSoftGreen,
                        borderRadius: BorderRadius.circular(9),
                      ),
                      child: const Icon(
                        Icons.landscape_rounded,
                        size: 19,
                        color: AppColors.figmaSecondary,
                      ),
                    ),
                    const SizedBox(width: 9),
                    Flexible(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Text(
                            'FAZENDA',
                            style: TextStyle(
                              color: AppColors.figmaText,
                              fontSize: 11,
                              fontWeight: FontWeight.w800,
                              letterSpacing: .5,
                              fontFamily: 'Poppins',
                            ),
                          ),
                          Text(
                            propertyName,
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                            style: const TextStyle(
                              color: AppColors.figmaSecondary,
                              fontSize: 12,
                              fontWeight: FontWeight.w600,
                              fontFamily: 'Poppins',
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 5),
                    const Icon(Icons.keyboard_arrow_down_rounded, size: 20),
                  ],
                ),
              ),
            ),
          ),
          Stack(
            children: [
              _HeaderButton(
                icon: Icons.notifications_rounded,
                onTap: onNotifications,
              ),
              const Positioned(
                top: 9,
                right: 9,
                child: DecoratedBox(
                  decoration: BoxDecoration(
                    color: Color(0xFFEA580C),
                    shape: BoxShape.circle,
                    border: Border.fromBorderSide(
                      BorderSide(color: Colors.white, width: 2),
                    ),
                  ),
                  child: SizedBox(width: 11, height: 11),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  static BoxDecoration _headerDecoration() => BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(10),
    border: Border.all(color: Colors.black.withValues(alpha: .04)),
    boxShadow: [
      BoxShadow(
        color: Colors.black.withValues(alpha: .05),
        blurRadius: 8,
        offset: const Offset(0, 6),
      ),
    ],
  );
}

class _HeaderButton extends StatelessWidget {
  const _HeaderButton({required this.icon, this.onTap});

  final IconData icon;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(10),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(10),
        child: Container(
          width: 42,
          height: 42,
          decoration: AgroFenceTopBar._headerDecoration(),
          child: Icon(icon, color: AppColors.figmaPrimary, size: 23),
        ),
      ),
    );
  }
}

class AgroFenceDrawer extends StatelessWidget {
  const AgroFenceDrawer({
    super.key,
    this.propertyName = 'Sabiá Dourado',
    this.currentRoute = AppRouter.home,
    this.onPropertySelected,
  });

  final String propertyName;
  final String currentRoute;
  final ValueChanged<RegisteredProperty>? onPropertySelected;

  @override
  Widget build(BuildContext context) {
    return Drawer(
      width: 328,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(),
      child: SafeArea(
        child: Column(
          children: [
            Container(
              width: double.infinity,
              padding: const EdgeInsets.fromLTRB(20, 18, 20, 22),
              color: AppColors.figmaPrimary700,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(
                        Icons.grid_on_rounded,
                        color: Colors.white,
                        size: 17,
                      ),
                      const SizedBox(width: 10),
                      const Text(
                        'AGROFENCE',
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.w800,
                          fontFamily: 'Poppins',
                          letterSpacing: .4,
                        ),
                      ),
                      const Spacer(),
                      IconButton.filledTonal(
                        onPressed: () => Navigator.pop(context),
                        icon: const Icon(Icons.close, color: Colors.white),
                        style: IconButton.styleFrom(
                          backgroundColor: Colors.white.withValues(alpha: .12),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10),
                            side: BorderSide(
                              color: Colors.white.withValues(alpha: .18),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 17),
                  Row(
                    children: [
                      const CircleAvatar(
                        radius: 28,
                        backgroundColor: AppColors.figmaSoftGreen,
                        child: Icon(
                          Icons.person,
                          color: AppColors.figmaPrimary700,
                        ),
                      ),
                      const SizedBox(width: 13),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'João Pereira',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 16,
                                fontWeight: FontWeight.w700,
                                fontFamily: 'Poppins',
                              ),
                            ),
                            InkWell(
                              onTap: () {
                                Navigator.pop(context);
                                showPropertySelectorSheet(
                                  context,
                                  currentPropertyName: propertyName,
                                  onSelected: onPropertySelected,
                                );
                              },
                              child: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  Flexible(
                                    child: Text(
                                      'Produtor · $propertyName',
                                      overflow: TextOverflow.ellipsis,
                                      style: TextStyle(
                                        color:
                                            Colors.white.withValues(alpha: .82),
                                        fontSize: 12,
                                      ),
                                    ),
                                  ),
                                  const SizedBox(width: 4),
                                  Icon(
                                    Icons.expand_more_rounded,
                                    size: 16,
                                    color: Colors.white.withValues(alpha: .82),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                      IconButton(
                        onPressed: () =>
                            Navigator.pushNamed(context, AppRouter.profile),
                        icon: const Icon(
                          Icons.edit_rounded,
                          color: Colors.white,
                          size: 17,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 18),
                  Row(
                    children: [
                      const Expanded(
                        child: _DrawerMetric(value: '10 mil', label: 'Animais'),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: InkWell(
                          onTap: () {
                            Navigator.pop(context);
                            Navigator.pushNamed(context, AppRouter.properties);
                          },
                          borderRadius: BorderRadius.circular(11),
                          child: const _DrawerMetric(
                            value: '3',
                            label: 'Fazendas',
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      const Expanded(
                        child: _DrawerMetric(value: '5', label: 'Alertas'),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            Expanded(
              child: ListView(
                padding: const EdgeInsets.fromLTRB(18, 20, 18, 14),
                children: [
                  const _DrawerLabel('MENU PRINCIPAL'),
                  _DrawerItem(
                    icon: Icons.home_rounded,
                    title: 'Home',
                    subtitle: 'Resumo da fazenda',
                    selected: currentRoute == AppRouter.home,
                    onTap: () => _replace(context, AppRouter.home),
                  ),
                  _DrawerItem(
                    icon: Icons.list_alt_rounded,
                    iconColor: const Color(0xFFEA580C),
                    iconBackground: const Color(0xFFFFEDD5),
                    title: 'Atividades',
                    subtitle: 'Tarefas e alertas do rebanho',
                    badge: '5',
                    selected: currentRoute == AppRouter.activities,
                    onTap: () => _replace(context, AppRouter.activities),
                  ),
                  _DrawerItem(
                    icon: Icons.landscape_rounded,
                    iconColor: AppColors.figmaSecondary,
                    iconBackground: AppColors.figmaSoftGreen,
                    title: 'Minhas Propriedades',
                    subtitle: 'Gerenciar fazendas',
                    selected: currentRoute == AppRouter.properties,
                    onTap: () => _replace(context, AppRouter.properties),
                  ),
                  _DrawerItem(
                    icon: Icons.apps_rounded,
                    iconColor: const Color(0xFF9333EA),
                    iconBackground: const Color(0xFFF3E8FF),
                    title: 'Módulos',
                    subtitle: 'Manejo, saúde, cercas e mais',
                    selected: currentRoute == AppRouter.modules,
                    onTap: () => _replace(context, AppRouter.modules),
                  ),
                  const _DrawerItem(
                    icon: Icons.query_stats_rounded,
                    iconColor: Color(0xFF16A34A),
                    iconBackground: Color(0xFFDCFCE7),
                    title: 'Relatórios',
                    subtitle: 'Indicadores e exportações',
                  ),
                  const _DrawerItem(
                    icon: Icons.support_agent_rounded,
                    iconColor: Color(0xFF3155B7),
                    iconBackground: Color(0xFFE0E7FF),
                    title: 'Suporte',
                    subtitle: 'Fale com nosso time',
                  ),
                  const Divider(height: 35),
                  const _DrawerLabel('CONTA'),
                  _DrawerItem(
                    icon: Icons.settings_rounded,
                    title: 'Configurações',
                    selected: currentRoute == AppRouter.appSettings,
                    onTap: () => _replace(context, AppRouter.appSettings),
                  ),
                  _DrawerItem(
                    icon: Icons.logout_rounded,
                    iconColor: Colors.red,
                    iconBackground: const Color(0xFFFEE2E2),
                    title: 'Sair da conta',
                    danger: true,
                    onTap: () => _logout(context),
                  ),
                  const SizedBox(height: 10),
                  const Center(
                    child: Text(
                      'AgroFence · v2.1.4',
                      style: TextStyle(color: Color(0xFF9CA3AF), fontSize: 11),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _replace(BuildContext context, String route) {
    Navigator.pop(context);
    if (currentRoute != route) {
      Navigator.pushReplacementNamed(context, route);
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

class _DrawerMetric extends StatelessWidget {
  const _DrawerMetric({required this.value, required this.label});
  final String value;
  final String label;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 8),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: .08),
        borderRadius: BorderRadius.circular(11),
        border: Border.all(color: Colors.white.withValues(alpha: .16)),
      ),
      child: Column(
        children: [
          Text(
            value,
            style: const TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.w800,
              fontSize: 16,
            ),
          ),
          Text(
            label,
            style: TextStyle(
              color: Colors.white.withValues(alpha: .8),
              fontSize: 10,
            ),
          ),
        ],
      ),
    );
  }
}

class _DrawerLabel extends StatelessWidget {
  const _DrawerLabel(this.text);
  final String text;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.fromLTRB(6, 0, 6, 7),
    child: Text(
      text,
      style: const TextStyle(
        color: Color(0xFF9CA3AF),
        fontSize: 10,
        fontWeight: FontWeight.w700,
        letterSpacing: .7,
      ),
    ),
  );
}

class _DrawerItem extends StatelessWidget {
  const _DrawerItem({
    required this.icon,
    required this.title,
    this.subtitle,
    this.iconColor = AppColors.figmaPrimary700,
    this.iconBackground = AppColors.figmaSoftGreen,
    this.selected = false,
    this.badge,
    this.danger = false,
    this.onTap,
  });

  final IconData icon;
  final String title;
  final String? subtitle;
  final Color iconColor;
  final Color iconBackground;
  final bool selected;
  final String? badge;
  final bool danger;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 220),
      curve: Curves.easeInOut,
      margin: const EdgeInsets.only(bottom: 4),
      decoration: BoxDecoration(
        color: selected
            ? AppColors.figmaSoftGreen
            : danger
            ? const Color(0xFFFEF2F2)
            : Colors.transparent,
        borderRadius: BorderRadius.circular(12),
        border: selected
            ? Border.all(
                color: AppColors.figmaSecondary.withValues(alpha: .35),
                width: 1.2,
              )
            : null,
      ),
      child: Material(
        color: Colors.transparent,
        borderRadius: BorderRadius.circular(12),
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(12),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 9),
            child: Row(
              children: [
                AnimatedContainer(
                  duration: const Duration(milliseconds: 220),
                  width: 38,
                  height: 38,
                  decoration: BoxDecoration(
                    color: selected
                        ? AppColors.figmaSecondary
                        : iconBackground,
                    borderRadius: BorderRadius.circular(11),
                  ),
                  child: Icon(
                    icon,
                    color: selected ? Colors.white : iconColor,
                    size: 19,
                  ),
                ),
                const SizedBox(width: 11),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: TextStyle(
                          color: danger
                              ? Colors.red
                              : selected
                              ? AppColors.figmaSecondary
                              : AppColors.figmaText,
                          fontWeight: selected
                              ? FontWeight.w800
                              : FontWeight.w700,
                          fontSize: 14,
                          fontFamily: 'Poppins',
                        ),
                      ),
                      if (subtitle != null)
                        Text(
                          subtitle!,
                          style: TextStyle(
                            color: selected
                                ? AppColors.figmaSecondary.withValues(
                                    alpha: .8,
                                  )
                                : AppColors.figmaMuted,
                            fontSize: 11,
                          ),
                        ),
                    ],
                  ),
                ),
                if (badge != null)
                  CircleAvatar(
                    radius: 10,
                    backgroundColor: Colors.red,
                    child: Text(
                      badge!,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  )
                else if (selected)
                  Container(
                    width: 7,
                    height: 7,
                    decoration: const BoxDecoration(
                      color: AppColors.figmaSecondary,
                      shape: BoxShape.circle,
                    ),
                  )
                else if (!danger)
                  const Icon(
                    Icons.chevron_right_rounded,
                    size: 18,
                    color: Color(0xFF9CA3AF),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class AgroFenceCard extends StatelessWidget {
  const AgroFenceCard({
    super.key,
    required this.child,
    this.padding = const EdgeInsets.all(16),
  });
  final Widget child;
  final EdgeInsetsGeometry padding;

  @override
  Widget build(BuildContext context) => Container(
    width: double.infinity,
    padding: padding,
    decoration: BoxDecoration(
      color: Colors.white,
      borderRadius: BorderRadius.circular(16),
      border: Border.all(color: Colors.black.withValues(alpha: .035)),
      boxShadow: [
        BoxShadow(
          color: Colors.black.withValues(alpha: .045),
          blurRadius: 15,
          offset: const Offset(0, 8),
        ),
      ],
    ),
    child: child,
  );
}

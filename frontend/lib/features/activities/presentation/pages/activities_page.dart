import 'package:ai_boi/core/data/operations_remote_data_source.dart';
import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/agrofence_shell.dart';
import 'package:ai_boi/features/activities/domain/entities/activity_module.dart';
import 'package:ai_boi/features/activities/presentation/pages/death_report_page.dart';
import 'package:ai_boi/features/activities/presentation/pages/health_record_page.dart';
import 'package:ai_boi/features/activities/presentation/pages/module_list_page.dart';
import 'package:ai_boi/features/activities/presentation/pages/module_placeholder_page.dart';
import 'package:ai_boi/features/activities/presentation/pages/reproduction_page.dart';
import 'package:ai_boi/features/activities/presentation/pages/weighing_page.dart';
import 'package:ai_boi/features/animals/presentation/pages/animals_list_page.dart';
import 'package:flutter/material.dart';

class ActivitiesPage extends StatelessWidget {
  const ActivitiesPage({
    super.key,
    required this.propertyId,
    required this.propertyName,
    required this.operations,
  });

  final int propertyId;
  final String propertyName;
  final OperationsRemoteDataSource operations;

  static const _groups = <_ActivityGroup>[
    _ActivityGroup(
      'Manejo',
      Icons.agriculture_rounded,
      AppColors.figmaSecondary,
      [
        _Action('Transferir Lote', Icons.swap_horiz_rounded),
        _Action(
          'Entrada Piquete',
          Icons.login_rounded,
          kind: ActivityModuleKind.animalEntry,
        ),
        _Action(
          'Saída Piquete',
          Icons.logout_rounded,
          kind: ActivityModuleKind.animalExit,
        ),
        _Action(
          'Suplementação',
          Icons.grass_rounded,
          kind: ActivityModuleKind.nutrition,
        ),
      ],
    ),
    _ActivityGroup('Reprodução', Icons.biotech_rounded, Color(0xFFDB2777), [
      _Action(
        'Registrar Cio',
        Icons.favorite_rounded,
        kind: ActivityModuleKind.reproduction,
      ),
      _Action(
        'Inseminação',
        Icons.biotech_rounded,
        kind: ActivityModuleKind.reproduction,
      ),
      _Action(
        'Diagnóstico',
        Icons.monitor_heart_rounded,
        kind: ActivityModuleKind.reproduction,
      ),
      _Action(
        'Registrar Parto',
        Icons.child_care_rounded,
        kind: ActivityModuleKind.births,
      ),
    ]),
    _ActivityGroup(
      'Sanidade',
      Icons.medical_services_rounded,
      Color(0xFFDC2626),
      [
        _Action(
          'Vacinação',
          Icons.vaccines_rounded,
          kind: ActivityModuleKind.health,
        ),
        _Action(
          'Vermifugação',
          Icons.coronavirus_rounded,
          kind: ActivityModuleKind.health,
        ),
        _Action(
          'Tratamentos',
          Icons.medication_rounded,
          kind: ActivityModuleKind.health,
        ),
        _Action(
          'Exames',
          Icons.science_rounded,
          kind: ActivityModuleKind.health,
        ),
      ],
    ),
    _ActivityGroup('Pesagem', Icons.monitor_weight_rounded, Color(0xFF3155B7), [
      _Action(
        'Nova Pesagem',
        Icons.monitor_weight_rounded,
        kind: ActivityModuleKind.weighAnimal,
      ),
      _Action(
        'Pesagem Lote',
        Icons.scale_rounded,
        kind: ActivityModuleKind.weighAnimal,
      ),
      _Action(
        'Avaliação Corp.',
        Icons.straighten_rounded,
        kind: ActivityModuleKind.weighAnimal,
      ),
      _Action(
        'Histórico Peso',
        Icons.history_rounded,
        kind: ActivityModuleKind.weighAnimal,
      ),
    ]),
    _ActivityGroup(
      'Financeiro',
      Icons.account_balance_wallet_rounded,
      Color(0xFF15803D),
      [
        _Action('Receitas', Icons.account_balance_rounded),
        _Action('Despesas', Icons.payments_rounded),
        _Action('Compra Insumos', Icons.shopping_cart_rounded),
        _Action('Fluxo de Caixa', Icons.query_stats_rounded),
      ],
    ),
    _ActivityGroup('Pastagem', Icons.grass_rounded, Color(0xFF65A30D), [
      _Action(
        'Avaliar Pasto',
        Icons.grass_rounded,
        kind: ActivityModuleKind.viewPastures,
      ),
      _Action(
        'Adubação',
        Icons.water_drop_rounded,
        kind: ActivityModuleKind.viewPastures,
      ),
      _Action(
        'Reforma',
        Icons.agriculture_rounded,
        kind: ActivityModuleKind.viewPastures,
      ),
      _Action(
        'Monitorar',
        Icons.visibility_rounded,
        kind: ActivityModuleKind.viewPastures,
      ),
    ]),
    _ActivityGroup(
      'Cercas Virtuais',
      Icons.satellite_alt_rounded,
      Color(0xFF2563EB),
      [
        _Action('Criar Cerca', Icons.draw_rounded),
        _Action('Editar Cerca', Icons.edit_location_alt_rounded),
        _Action('Visualizar Mapa', Icons.map_rounded),
        _Action('Alertas/Fugas', Icons.warning_rounded),
      ],
    ),
  ];

  @override
  Widget build(BuildContext context) {
    final scaffoldKey = GlobalKey<ScaffoldState>();
    return Scaffold(
      key: scaffoldKey,
      backgroundColor: Colors.white,
      drawer: AgroFenceDrawer(
        propertyName: propertyName,
        currentRoute: AppRouter.activities,
        onPropertySelected: (prop) => Navigator.pushReplacementNamed(
          context,
          AppRouter.activities,
          arguments: {
            'propertyId': prop.id,
            'propertyName': prop.name,
          },
        ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(18, 18, 18, 8),
              child: Row(
                children: [
                  IconButton.outlined(
                    onPressed: () => scaffoldKey.currentState?.openDrawer(),
                    icon: const Icon(Icons.menu_rounded, size: 20),
                    style: IconButton.styleFrom(
                      side: const BorderSide(color: AppColors.figmaBorder),
                    ),
                  ),
                  const Expanded(
                    child: Text(
                      'Atividades',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: AppColors.figmaPrimary,
                        fontSize: 17,
                        fontWeight: FontWeight.w800,
                        fontFamily: 'Poppins',
                      ),
                    ),
                  ),
                  IconButton.outlined(
                    onPressed: () {},
                    icon: const Icon(Icons.search_rounded, size: 20),
                    style: IconButton.styleFrom(
                      side: const BorderSide(color: AppColors.figmaBorder),
                    ),
                  ),
                ],
              ),
            ),
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 24),
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'Escolha uma atividade para começar.',
                  style: TextStyle(color: AppColors.figmaMuted, fontSize: 12),
                ),
              ),
            ),
            const SizedBox(height: 7),
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.fromLTRB(0, 0, 0, 14),
                itemCount: _groups.length + 1,
                itemBuilder: (context, index) {
                  if (index == _groups.length) {
                    return Container(
                      margin: const EdgeInsets.fromLTRB(18, 8, 18, 0),
                      padding: const EdgeInsets.symmetric(
                        horizontal: 14,
                        vertical: 10,
                      ),
                      decoration: BoxDecoration(
                        color: const Color(0xFFF0FFF4),
                        borderRadius: BorderRadius.circular(11),
                        border: Border.all(color: const Color(0xFFC6F6D5)),
                      ),
                      child: const Row(
                        children: [
                          Icon(
                            Icons.info,
                            color: AppColors.figmaPrimary700,
                            size: 16,
                          ),
                          SizedBox(width: 10),
                          Expanded(
                            child: Text(
                              'Deslize para a esquerda para ver mais\natividades de cada grupo.',
                              style: TextStyle(
                                color: AppColors.figmaPrimary,
                                fontSize: 10,
                              ),
                            ),
                          ),
                          Icon(
                            Icons.swipe_left_rounded,
                            color: AppColors.figmaPrimary700,
                            size: 18,
                          ),
                        ],
                      ),
                    );
                  }
                  final group = _groups[index];
                  return _GroupSection(
                    group: group,
                    onTap: (action) => _openAction(context, action),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _openAction(BuildContext context, _Action action) {
    final kind = action.kind;
    if (kind == null) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) =>
              ModulePlaceholderPage(title: action.label, rfCode: 'Em evolução'),
        ),
      );
      return;
    }
    final module = ActivityModule.defaults.firstWhere(
      (m) => m.kind == kind,
      orElse: () => ActivityModule(
        kind: kind,
        label: action.label,
        icon: action.icon,
        backgroundColor: AppColors.figmaSoftGreen,
        rfCode: 'MVP',
      ),
    );
    if (!module.apiReady) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => ModulePlaceholderPage(
            title: action.label,
            rfCode: module.rfCode,
            message: 'Este módulo ainda não possui endpoint no backend.',
          ),
        ),
      );
      return;
    }
    switch (kind) {
      case ActivityModuleKind.viewAnimals:
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => AnimalsListPage(
              propertyId: propertyId,
              propertyName: propertyName,
            ),
          ),
        );
      case ActivityModuleKind.viewPastures:
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ModuleListPage(
              title: action.label,
              rfCode: module.rfCode,
              load: () async =>
                  ((await operations.listPastures(propertyId: propertyId))
                              as List? ??
                          [])
                      .cast<Map<String, dynamic>>(),
              itemTitle: (row) => row['name']?.toString() ?? 'Pastagem',
              itemSubtitle: (row) =>
                  '${row['area']} ha · cap. ${row['capacity']}',
            ),
          ),
        );
      case ActivityModuleKind.health:
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => HealthRecordPage(
              propertyId: propertyId,
              propertyName: propertyName,
            ),
          ),
        );
      case ActivityModuleKind.reproduction || ActivityModuleKind.births:
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ReproductionPage(
              propertyId: propertyId,
              propertyName: propertyName,
            ),
          ),
        );
      case ActivityModuleKind.deathReport:
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => DeathReportPage(
              propertyId: propertyId,
              propertyName: propertyName,
            ),
          ),
        );
      case ActivityModuleKind.weighAnimal:
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => WeighingPage(
              propertyId: propertyId,
              propertyName: propertyName,
            ),
          ),
        );
      default:
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ModulePlaceholderPage(
              title: action.label,
              rfCode: module.rfCode,
            ),
          ),
        );
    }
  }
}

class _GroupSection extends StatelessWidget {
  const _GroupSection({required this.group, required this.onTap});
  final _ActivityGroup group;
  final ValueChanged<_Action> onTap;
  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(top: 9),
    child: Column(
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: Row(
            children: [
              Icon(group.icon, color: group.color, size: 16),
              const SizedBox(width: 8),
              Text(
                group.title,
                style: const TextStyle(
                  color: AppColors.figmaPrimary,
                  fontSize: 13,
                  fontWeight: FontWeight.w800,
                  fontFamily: 'Poppins',
                ),
              ),
              const Spacer(),
              TextButton.icon(
                onPressed: () {},
                iconAlignment: IconAlignment.end,
                icon: const Icon(Icons.chevron_right, size: 14),
                label: const Text('Ver tudo'),
                style: TextButton.styleFrom(
                  foregroundColor: const Color(0xFF7BAA7A),
                  textStyle: const TextStyle(fontSize: 10),
                ),
              ),
            ],
          ),
        ),
        SizedBox(
          height: 94,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 20),
            itemCount: group.actions.length,
            separatorBuilder: (_, _) => const SizedBox(width: 8),
            itemBuilder: (_, index) => _ActionTile(
              action: group.actions[index],
              color: group.color,
              onTap: () => onTap(group.actions[index]),
            ),
          ),
        ),
        const SizedBox(height: 7),
        const Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [_PagerDot(active: true), _PagerDot()],
        ),
      ],
    ),
  );
}

class _ActionTile extends StatelessWidget {
  const _ActionTile({
    required this.action,
    required this.color,
    required this.onTap,
  });
  final _Action action;
  final Color color;
  final VoidCallback onTap;
  @override
  Widget build(BuildContext context) => InkWell(
    onTap: onTap,
    borderRadius: BorderRadius.circular(12),
    child: Container(
      width: 88,
      padding: const EdgeInsets.fromLTRB(6, 10, 6, 7),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.figmaBorder),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: .035),
            blurRadius: 7,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: Column(
        children: [
          Container(
            width: 42,
            height: 42,
            decoration: BoxDecoration(
              color: color.withValues(alpha: .11),
              borderRadius: BorderRadius.circular(11),
            ),
            child: Icon(action.icon, color: color, size: 20),
          ),
          const SizedBox(height: 7),
          Text(
            action.label,
            textAlign: TextAlign.center,
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
            style: const TextStyle(
              color: AppColors.figmaText,
              fontSize: 9,
              height: 1.15,
            ),
          ),
        ],
      ),
    ),
  );
}

class _PagerDot extends StatelessWidget {
  const _PagerDot({this.active = false});
  final bool active;
  @override
  Widget build(BuildContext context) => Container(
    width: active ? 6 : 4,
    height: 4,
    margin: const EdgeInsets.symmetric(horizontal: 2),
    decoration: BoxDecoration(
      color: active ? const Color(0xFF7BAA7A) : AppColors.figmaBorder,
      borderRadius: BorderRadius.circular(4),
    ),
  );
}

class _ActivityGroup {
  const _ActivityGroup(this.title, this.icon, this.color, this.actions);
  final String title;
  final IconData icon;
  final Color color;
  final List<_Action> actions;
}

class _Action {
  const _Action(this.label, this.icon, {this.kind});
  final String label;
  final IconData icon;
  final ActivityModuleKind? kind;
}

import 'package:ai_boi/core/data/operations_remote_data_source.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/features/activities/domain/entities/activity_module.dart';
import 'package:ai_boi/features/activities/presentation/pages/module_list_page.dart';
import 'package:ai_boi/features/activities/presentation/pages/module_placeholder_page.dart';
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

  void _openModule(BuildContext context, ActivityModule module) {
    if (!module.apiReady) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => ModulePlaceholderPage(
            title: module.label,
            rfCode: module.rfCode,
            message:
                'Este módulo (${module.rfCode}) ainda não possui endpoint no backend.',
          ),
        ),
      );
      return;
    }

    switch (module.kind) {
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
              title: module.label,
              rfCode: module.rfCode,
              load: () async {
                final result = await operations.listPastures(propertyId: propertyId);
                return (result as List? ?? []).cast<Map<String, dynamic>>();
              },
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
            builder: (_) => ModuleListPage(
              title: module.label,
              rfCode: module.rfCode,
              load: () async {
                final result = await operations.listHealthRecords();
                return (result as List? ?? []).cast<Map<String, dynamic>>();
              },
              itemTitle: (row) =>
                  row['treatment_type']?.toString() ?? 'Registro de saúde',
              itemSubtitle: (row) =>
                  'Animal #${row['animal_id']} · ${row['application_date'] ?? ''}',
            ),
          ),
        );
      case ActivityModuleKind.reproduction:
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ModuleListPage(
              title: module.label,
              rfCode: module.rfCode,
              load: () async {
                final result = await operations.listReproductions();
                return (result as List? ?? []).cast<Map<String, dynamic>>();
              },
              itemTitle: (row) =>
                  'Reprodução #${row['id_reproduction'] ?? row['id']}',
              itemSubtitle: (row) =>
                  row['status']?.toString() ?? 'Em acompanhamento',
            ),
          ),
        );
      case ActivityModuleKind.births:
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ModulePlaceholderPage(
              title: module.label,
              rfCode: module.rfCode,
              message:
                  'Registre nascimentos via POST /reproductions/{id}/birth.\n'
                  'Selecione uma reprodução na tela Reprodução para registrar.',
              actionLabel: 'Ver reproduções',
              onAction: () => _openModule(
                context,
                ActivityModule.defaults.firstWhere(
                  (m) => m.kind == ActivityModuleKind.reproduction,
                ),
              ),
            ),
          ),
        );
      case ActivityModuleKind.deathReport:
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ModulePlaceholderPage(
              title: module.label,
              rfCode: module.rfCode,
              message:
                  'Atualize animal_life_status via PUT /animals/{id}.\n'
                  'Formulário de óbito em desenvolvimento.',
              actionLabel: 'Ver animais',
              onAction: () => _openModule(
                context,
                ActivityModule.defaults.firstWhere(
                  (m) => m.kind == ActivityModuleKind.viewAnimals,
                ),
              ),
            ),
          ),
        );
      case ActivityModuleKind.weighAnimal:
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ModulePlaceholderPage(
              title: module.label,
              rfCode: module.rfCode,
              message:
                  'Pesagens via POST /weighings/ e GET /weighings/animal/{id}.\n'
                  'Integração com balança digital (RF024) em desenvolvimento.',
              actionLabel: 'Ver animais',
              onAction: () => _openModule(
                context,
                ActivityModule.defaults.firstWhere(
                  (m) => m.kind == ActivityModuleKind.viewAnimals,
                ),
              ),
            ),
          ),
        );
      default:
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ModulePlaceholderPage(
              title: module.label,
              rfCode: module.rfCode,
            ),
          ),
        );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: const BoxDecoration(color: AppColors.primaryButton),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  Text(
                    propertyName,
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      fontFamily: 'Poppins',
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Propriedade #$propertyId',
                    style: TextStyle(
                      color: Colors.white.withValues(alpha: 0.85),
                      fontFamily: 'Poppins',
                    ),
                  ),
                ],
              ),
            ),
            ListTile(
              leading: const Icon(Icons.home_outlined),
              title: const Text('Minhas propriedades'),
              onTap: () {
                Navigator.pop(context);
                Navigator.pop(context);
              },
            ),
          ],
        ),
      ),
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        iconTheme: const IconThemeData(color: AppColors.textPrimary),
        title: const Text(
          'Atividades',
          style: TextStyle(
            color: Color(0xFF1E3A5F),
            fontWeight: FontWeight.bold,
            fontSize: 20,
            fontFamily: 'Poppins',
          ),
        ),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        child: GridView.builder(
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            mainAxisSpacing: 12,
            crossAxisSpacing: 12,
            childAspectRatio: 0.95,
          ),
          itemCount: ActivityModule.defaults.length,
          itemBuilder: (context, index) {
            final module = ActivityModule.defaults[index];
            return _ActivityTile(
              module: module,
              onTap: () => _openModule(context, module),
            );
          },
        ),
      ),
    );
  }
}

class _ActivityTile extends StatelessWidget {
  const _ActivityTile({required this.module, required this.onTap});

  final ActivityModule module;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final enabled = module.apiReady;

    return Material(
      color: module.backgroundColor,
      borderRadius: BorderRadius.circular(16),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        overlayColor: WidgetStateProperty.resolveWith((states) {
          if (states.contains(WidgetState.pressed)) {
            return AppColors.primaryButton.withValues(alpha: 0.12);
          }
          if (states.contains(WidgetState.hovered)) {
            return AppColors.primaryButtonHover.withValues(alpha: 0.15);
          }
          return null;
        }),
        child: Opacity(
          opacity: enabled ? 1 : 0.65,
          child: Padding(
            padding: const EdgeInsets.all(14),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  module.icon,
                  size: 40,
                  color: enabled
                      ? AppColors.primaryButton
                      : AppColors.buttonDisabled,
                ),
                const SizedBox(height: 10),
                Text(
                  module.label,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                    color: enabled
                        ? const Color(0xFF1E3A5F)
                        : AppColors.buttonDisabled,
                    fontFamily: 'Poppins',
                    height: 1.2,
                  ),
                ),
                if (!enabled) ...[
                  const SizedBox(height: 4),
                  Text(
                    'Em breve',
                    style: TextStyle(
                      fontSize: 10,
                      color: AppColors.buttonDisabled,
                      fontFamily: 'Poppins',
                    ),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}


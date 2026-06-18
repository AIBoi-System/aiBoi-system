import 'package:flutter/material.dart';

/// Módulo exibido na grade de Atividades, mapeado aos RFs do sistema.
enum ActivityModuleKind {
  births, // RF003 / RF005
  deathReport, // RF003
  nutrition, // RF007 — backend pendente
  health, // RF006
  animalEntry, // RF012 — backend pendente
  animalExit, // RF012 — backend pendente
  viewAnimals, // RF003
  viewPastures, // RF009
  weighAnimal, // RF024
  reproduction, // RF005
}

class ActivityModule {
  final ActivityModuleKind kind;
  final String label;
  final IconData icon;
  final Color backgroundColor;
  final String rfCode;
  final bool apiReady;

  const ActivityModule({
    required this.kind,
    required this.label,
    required this.icon,
    required this.backgroundColor,
    required this.rfCode,
    this.apiReady = true,
  });

  static const List<ActivityModule> defaults = [
    ActivityModule(
      kind: ActivityModuleKind.births,
      label: 'Nascimentos',
      icon: Icons.child_care_outlined,
      backgroundColor: Color(0xFFD4EDDA),
      rfCode: 'RF003/RF005',
      apiReady: true,
    ),
    ActivityModule(
      kind: ActivityModuleKind.deathReport,
      label: 'Informar Morte',
      icon: Icons.dangerous_outlined,
      backgroundColor: Color(0xFFF8D7DA),
      rfCode: 'RF003',
      apiReady: true,
    ),
    ActivityModule(
      kind: ActivityModuleKind.nutrition,
      label: 'Realizar Nutrição',
      icon: Icons.grass_outlined,
      backgroundColor: Color(0xFFD1ECF1),
      rfCode: 'RF007',
      apiReady: false,
    ),
    ActivityModule(
      kind: ActivityModuleKind.health,
      label: 'Saúde Animal',
      icon: Icons.medical_services_outlined,
      backgroundColor: Color(0xFFD4EDDA),
      rfCode: 'RF006',
      apiReady: true,
    ),
    ActivityModule(
      kind: ActivityModuleKind.animalEntry,
      label: 'Registrar Entrada',
      icon: Icons.login_outlined,
      backgroundColor: Color(0xFFFFE5CC),
      rfCode: 'RF012',
      apiReady: false,
    ),
    ActivityModule(
      kind: ActivityModuleKind.animalExit,
      label: 'Registrar Saída',
      icon: Icons.logout_outlined,
      backgroundColor: Color(0xFFD6EAF8),
      rfCode: 'RF012',
      apiReady: false,
    ),
    ActivityModule(
      kind: ActivityModuleKind.viewAnimals,
      label: 'Ver Animais',
      icon: Icons.pets_outlined,
      backgroundColor: Color(0xFFFFE5CC),
      rfCode: 'RF003',
      apiReady: true,
    ),
    ActivityModule(
      kind: ActivityModuleKind.viewPastures,
      label: 'Ver Pastagens',
      icon: Icons.eco_outlined,
      backgroundColor: Color(0xFFD4EDDA),
      rfCode: 'RF009',
      apiReady: true,
    ),
    ActivityModule(
      kind: ActivityModuleKind.weighAnimal,
      label: 'Pesar animal',
      icon: Icons.monitor_weight_outlined,
      backgroundColor: Color(0xFFFFE5CC),
      rfCode: 'RF024',
      apiReady: true,
    ),
    ActivityModule(
      kind: ActivityModuleKind.reproduction,
      label: 'Reprodução',
      icon: Icons.biotech_outlined,
      backgroundColor: Color(0xFFF8D7DA),
      rfCode: 'RF005',
      apiReady: true,
    ),
  ];
}


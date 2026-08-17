import 'package:flutter/material.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/agrofence_shell.dart';
import 'package:ai_boi/core/navigation/app_router.dart';

class ModulesPage extends StatelessWidget {
  const ModulesPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.backgroundScreen,
      drawer: const AgroFenceDrawer(currentRoute: AppRouter.modules),
      body: SafeArea(
        child: Column(
          children: [
            Builder(
              builder: (context) => AgroFenceTopBar(
                propertyName: 'Sabiá Dourado', // Dummy fallback, real app would fetch from state
                onMenu: () => Scaffold.of(context).openDrawer(),
              ),
            ),
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(24),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
              'Meus Módulos',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                fontFamily: 'Poppins',
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              'Gerencie as funcionalidades ativas na sua fazenda.',
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),
            const SizedBox(height: 24),
            _buildModuleCard(
              context: context,
              icon: Icons.pets_rounded,
              iconColor: AppColors.primaryButton,
              iconBgColor: AppColors.primaryButton.withValues(alpha: 0.1),
              title: 'Gestão de Animais',
              description: 'Cadastro, saúde, pesos e relatórios zootécnicos do rebanho.',
              status: 'Ativo',
              statusColor: Colors.green,
            ),
            const SizedBox(height: 16),
            _buildModuleCard(
              context: context,
              icon: Icons.attach_money_rounded,
              iconColor: const Color(0xFFEAB308),
              iconBgColor: const Color(0xFFFEF9C3),
              title: 'Financeiro',
              description: 'Controle de receitas, despesas e fluxo de caixa da propriedade.',
              status: 'Ativar',
              statusColor: Colors.blue,
            ),
            const SizedBox(height: 16),
            _buildModuleCard(
              context: context,
              icon: Icons.agriculture_rounded,
              iconColor: const Color(0xFF8B5CF6),
              iconBgColor: const Color(0xFFEDE9FE),
              title: 'Maquinário',
              description: 'Manutenção, consumo e uso de tratores e implementos.',
              status: 'Ativar',
              statusColor: Colors.blue,
            ),
          ],
        ),
      ),
      ),
        ],
      ),
      ),
    );
  }

  Widget _buildModuleCard({
    required BuildContext context,
    required IconData icon,
    required Color iconColor,
    required Color iconBgColor,
    required String title,
    required String description,
    required String status,
    required Color statusColor,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.shade200),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  color: iconBgColor,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Icon(icon, color: iconColor),
              ),
              const Spacer(),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: statusColor.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  status,
                  style: TextStyle(
                    color: statusColor,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            title,
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              fontFamily: 'Poppins',
            ),
          ),
          const SizedBox(height: 8),
          Text(
            description,
            style: const TextStyle(fontSize: 14, color: Colors.grey),
          ),
          const SizedBox(height: 16),
          SizedBox(
            width: double.infinity,
            child: OutlinedButton(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Ação: $status módulo $title')),
                );
              },
              style: OutlinedButton.styleFrom(
                side: BorderSide(color: Colors.grey.shade300),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
              child: const Text(
                'Acessar',
                style: TextStyle(color: Colors.black87),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

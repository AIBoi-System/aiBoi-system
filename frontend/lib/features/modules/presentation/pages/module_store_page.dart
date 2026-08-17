import 'package:flutter/material.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/widgets/agrofence_shell.dart';

class ModuleStorePage extends StatelessWidget {
  const ModuleStorePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.backgroundScreen,
      drawer: const AgroFenceDrawer(currentRoute: AppRouter.moduleStore),
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.transparent,
        foregroundColor: Colors.black,
        title: const Text('Área de Módulo', style: TextStyle(fontFamily: 'Poppins')),
        centerTitle: true,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_rounded),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: const [
              _Header(),
              SizedBox(height: 24),
              _FilterChips(),
              SizedBox(height: 24),
              _SummaryCards(),
              SizedBox(height: 24),
              Text('Módulos Ativos', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, fontFamily: 'Poppins')),
              SizedBox(height: 12),
              _ActiveModulesList(),
              SizedBox(height: 24),
              Text('Módulos Disponíveis', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, fontFamily: 'Poppins')),
              SizedBox(height: 12),
              _AvailableModulesList(),
            ],
          ),
        ),
      ),
    );
  }
}

class _Header extends StatelessWidget {
  const _Header();
  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: const [
        Text('Expanda o aiBoi do seu jeito', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, fontFamily: 'Poppins')),
        SizedBox(height: 8),
        Text('Encontre módulos que atendam às necessidades da sua fazenda e aumente a eficiência.', style: TextStyle(fontSize: 14, color: Colors.grey)),
      ],
    );
  }
}

class _FilterChips extends StatefulWidget {
  const _FilterChips({Key? key}) : super(key: key);
  @override
  State<_FilterChips> createState() => _FilterChipsState();
}

class _FilterChipsState extends State<_FilterChips> {
  final List<String> _options = ['Todos', 'Manejo', 'Saúde', 'Financeiro'];
  String _selected = 'Todos';
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: Row(
        children: _options.map((opt) {
          final bool isSelected = opt == _selected;
          return Padding(
            padding: const EdgeInsets.only(right: 8),
            child: ChoiceChip(
              label: Text(opt, style: const TextStyle(fontFamily: 'Poppins')),
              selected: isSelected,
              selectedColor: AppColors.primaryButton,
              backgroundColor: Colors.transparent,
              shape: StadiumBorder(side: BorderSide(color: isSelected ? Colors.transparent : AppColors.primaryButton)),
              onSelected: (_) => setState(() => _selected = opt),
            ),
          );
        }).toList(),
      ),
    );
  }
}

class _SummaryCards extends StatelessWidget {
  const _SummaryCards();
  @override
  Widget build(BuildContext context) {
    return Row(
      children: const [
        _SummaryCard(title: 'Ativos', count: 3, buttonLabel: 'Ver meus módulos'),
        SizedBox(width: 16),
        _SummaryCard(title: 'Disponíveis', count: 8, buttonLabel: 'Ver todos'),
      ],
    );
  }
}

class _SummaryCard extends StatelessWidget {
  final String title;
  final int count;
  final String buttonLabel;
  const _SummaryCard({Key? key, required this.title, required this.count, required this.buttonLabel}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: Colors.grey.shade200),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600, fontFamily: 'Poppins')),
            const SizedBox(height: 4),
            Text('$count', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, fontFamily: 'Poppins')),
            const SizedBox(height: 12),
            OutlinedButton(
              onPressed: () {},
              style: OutlinedButton.styleFrom(padding: const EdgeInsets.symmetric(vertical: 8)),
              child: Text(buttonLabel, style: const TextStyle(fontFamily: 'Poppins')),
            ),
          ],
        ),
      ),
    );
  }
}

class _ActiveModulesList extends StatelessWidget {
  const _ActiveModulesList();
  @override
  Widget build(BuildContext context) {
    final List<Map<String, dynamic>> modules = [
      {'icon': Icons.pets_rounded, 'color': AppColors.primaryButton, 'title': 'Gestão de Animais', 'desc': 'Cadastro e saúde do rebanho', 'status': 'Ativo', 'statusColor': Colors.green},
      {'icon': Icons.attach_money_rounded, 'color': Color(0xFFEAB308), 'title': 'Financeiro', 'desc': 'Fluxo de caixa', 'status': 'Ativo', 'statusColor': Colors.blue},
    ];
    return Column(
      children: modules.map((m) => _ModuleCard(
        icon: m['icon'],
        iconColor: m['color'],
        title: m['title'],
        description: m['desc'],
        status: m['status'],
        statusColor: m['statusColor'],
        isAvailable: false,
      )).toList(),
    );
  }
}

class _AvailableModulesList extends StatelessWidget {
  const _AvailableModulesList();
  @override
  Widget build(BuildContext context) {
    final List<Map<String, dynamic>> modules = [
      {'icon': Icons.agriculture_rounded, 'color': Color(0xFF8B5CF6), 'title': 'Monitoramento de Máquinas', 'price': 'R\$ 49,90/mês'},
      {'icon': Icons.auto_awesome, 'color': Color(0xFFEF4444), 'title': 'Sensores IoT', 'price': 'R\$ 29,90/mês'},
    ];
    return Column(
      children: modules.map((m) => _AvailableModuleCard(
        icon: m['icon'],
        iconColor: m['color'],
        title: m['title'],
        price: m['price'],
      )).toList(),
    );
  }
}

class _ModuleCard extends StatelessWidget {
  final IconData icon;
  final Color iconColor;
  final String title;
  final String description;
  final String status;
  final Color statusColor;
  final bool isAvailable;
  const _ModuleCard({Key? key, required this.icon, required this.iconColor, required this.title, required this.description, required this.status, required this.statusColor, required this.isAvailable}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
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
                decoration: BoxDecoration(color: iconColor.withValues(alpha: 0.1), borderRadius: BorderRadius.circular(8)),
                child: Icon(icon, color: iconColor),
              ),
              const Spacer(),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(color: statusColor.withValues(alpha: 0.1), borderRadius: BorderRadius.circular(20)),
                child: Text(status, style: TextStyle(color: statusColor, fontSize: 12, fontWeight: FontWeight.bold)),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, fontFamily: 'Poppins')),
          const SizedBox(height: 8),
          Text(description, style: const TextStyle(fontSize: 14, color: Colors.grey)),
          const SizedBox(height: 16),
          SizedBox(
            width: double.infinity,
            child: OutlinedButton(
              onPressed: () {},
              child: const Text('Acessar', style: TextStyle(color: Colors.black87)),
            ),
          ),
        ],
      ),
    );
  }
}

class _AvailableModuleCard extends StatelessWidget {
  final IconData icon;
  final Color iconColor;
  final String title;
  final String price;
  const _AvailableModuleCard({Key? key, required this.icon, required this.iconColor, required this.title, required this.price}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
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
                decoration: BoxDecoration(color: iconColor.withValues(alpha: 0.1), borderRadius: BorderRadius.circular(8)),
                child: Icon(icon, color: iconColor),
              ),
              const Spacer(),
              Text(price, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
            ],
          ),
          const SizedBox(height: 16),
          Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, fontFamily: 'Poppins')),
          const SizedBox(height: 8),
          const Text('Descrição curta do módulo.', style: TextStyle(fontSize: 14, color: Colors.grey)),
          const SizedBox(height: 16),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: () {},
              child: const Text('Adicionar'),
            ),
          ),
        ],
      ),
    );
  }
}

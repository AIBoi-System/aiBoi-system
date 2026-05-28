import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';
import 'package:flutter/material.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key, this.properties = const []});

  final List<RegisteredProperty> properties;

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _tabIndex = 0;
  final List<RegisteredProperty> _properties = [];

  @override
  void initState() {
    super.initState();
    _properties.addAll(widget.properties);
    if (_properties.isEmpty) {
      _properties.add(
        const RegisteredProperty(
          id: 1,
          name: 'Sabiá dourado',
          cityState: 'Anapu - PA',
          purpose: 'Genética',
          hectares: 1000,
        ),
      );
    }
  }

  List<RegisteredProperty> get _filtered {
    if (_tabIndex == 1) return [];
    return _properties;
  }

  @override
  Widget build(BuildContext context) {
    final args = ModalRoute.of(context)?.settings.arguments;
    if (args is RegisteredProperty && !_properties.any((p) => p.id == args.id)) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        setState(() => _properties.insert(0, args));
      });
    }

    return Scaffold(
      backgroundColor: AppColors.backgroundScreen,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 8),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'aiboi',
                    style: TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: AppColors.primaryGreen,
                      fontFamily: 'Poppins',
                    ),
                  ),
                  CircleAvatar(
                    radius: 20,
                    backgroundColor: Colors.grey.shade300,
                    child: const Icon(Icons.person, color: Colors.white),
                  ),
                ],
              ),
              const SizedBox(height: 20),
              const Text(
                'Minhas Propriedades',
                style: TextStyle(
                  fontSize: 26,
                  fontWeight: FontWeight.bold,
                  color: AppColors.primaryGreen,
                  fontFamily: 'Poppins',
                ),
              ),
              const SizedBox(height: 8),
              const Text(
                'Gerencie suas fazendas de forma simples e organizada',
                style: TextStyle(
                  color: AppColors.textSecondary,
                  fontSize: 14,
                  fontFamily: 'Poppins',
                ),
              ),
              const SizedBox(height: 20),
              Row(
                children: [
                  Expanded(
                    child: Container(
                      padding: const EdgeInsets.symmetric(vertical: 4),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(24),
                      ),
                      child: Row(
                        children: [
                          _TabChip(
                            label: 'Ativas',
                            selected: _tabIndex == 0,
                            onTap: () => setState(() => _tabIndex = 0),
                          ),
                          _TabChip(
                            label: 'Inativas',
                            selected: _tabIndex == 1,
                            onTap: () => setState(() => _tabIndex = 1),
                          ),
                          _TabChip(
                            label: 'Buscar',
                            selected: _tabIndex == 2,
                            onTap: () => setState(() => _tabIndex = 2),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Material(
                    color: AppColors.primaryGreen,
                    borderRadius: BorderRadius.circular(12),
                    child: InkWell(
                      onTap: () async {
                        await Navigator.pushNamed(context, AppRouter.propertyCreate);
                      },
                      borderRadius: BorderRadius.circular(12),
                      child: const SizedBox(
                        width: 48,
                        height: 48,
                        child: Icon(Icons.add, color: Colors.white),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 20),
              Expanded(
                child: _filtered.isEmpty
                    ? Center(
                        child: Text(
                          _tabIndex == 1
                              ? 'Nenhuma propriedade inativa'
                              : 'Nenhuma propriedade encontrada',
                          style: const TextStyle(
                            color: AppColors.textSecondary,
                            fontFamily: 'Poppins',
                          ),
                        ),
                      )
                    : ListView.builder(
                        itemCount: _filtered.length,
                        itemBuilder: (context, index) {
                          final p = _filtered[index];
                          return _PropertyCard(property: p);
                        },
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _TabChip extends StatelessWidget {
  final String label;
  final bool selected;
  final VoidCallback onTap;

  const _TabChip({
    required this.label,
    required this.selected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 10),
          decoration: BoxDecoration(
            border: selected
                ? const Border(
                    bottom: BorderSide(color: AppColors.primaryGreen, width: 2),
                  )
                : null,
          ),
          child: Text(
            label,
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: 12,
              fontWeight: selected ? FontWeight.w600 : FontWeight.normal,
              color: selected ? AppColors.primaryGreen : AppColors.textSecondary,
              fontFamily: 'Poppins',
            ),
          ),
        ),
      ),
    );
  }
}

class _PropertyCard extends StatelessWidget {
  final RegisteredProperty property;

  const _PropertyCard({required this.property});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            width: 72,
            height: 72,
            decoration: BoxDecoration(
              color: AppColors.progressActive.withValues(alpha: 0.3),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Icon(Icons.landscape, color: AppColors.primaryGreen, size: 36),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  property.name,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                    fontFamily: 'Poppins',
                  ),
                ),
                const SizedBox(height: 8),
                _DetailRow(Icons.location_on_outlined, property.cityState),
                _DetailRow(Icons.category_outlined, 'Finalidade: ${property.purpose}'),
                _DetailRow(Icons.pets_outlined, '— animais'),
                _DetailRow(
                  Icons.square_foot_outlined,
                  '${property.hectares.toStringAsFixed(0)} hectares',
                ),
              ],
            ),
          ),
          Column(
            children: [
              const Icon(Icons.more_vert, color: AppColors.textSecondary),
              const SizedBox(height: 24),
              CircleAvatar(
                radius: 18,
                backgroundColor: AppColors.progressActive.withValues(alpha: 0.3),
                child: const Icon(
                  Icons.arrow_forward,
                  size: 18,
                  color: AppColors.primaryGreen,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _DetailRow extends StatelessWidget {
  final IconData icon;
  final String text;

  const _DetailRow(this.icon, this.text);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 4),
      child: Row(
        children: [
          Icon(icon, size: 14, color: AppColors.textSecondary),
          const SizedBox(width: 6),
          Expanded(
            child: Text(
              text,
              style: const TextStyle(
                fontSize: 12,
                color: AppColors.textSecondary,
                fontFamily: 'Poppins',
              ),
            ),
          ),
        ],
      ),
    );
  }
}

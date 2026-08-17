import 'package:ai_boi/core/di/app_bindings.dart';
import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/agrofence_shell.dart';
import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';
import 'package:flutter/material.dart';

class PropertiesPage extends StatefulWidget {
  const PropertiesPage({super.key});
  @override
  State<PropertiesPage> createState() => _PropertiesPageState();
}

class _PropertiesPageState extends State<PropertiesPage> {
  final _scaffoldKey = GlobalKey<ScaffoldState>();
  List<RegisteredProperty> _properties = const [];
  bool _loading = true;
  String? _error;
  int _filter = 0;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final result = await AppBindings.propertyRepository().listProperties();
      if (mounted) setState(() => _properties = result);
    } catch (error) {
      if (mounted) setState(() => _error = error.toString());
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final propertyName = _properties.isEmpty
        ? 'Sabiá Dourado'
        : _properties.first.name;
    return Scaffold(
      key: _scaffoldKey,
      backgroundColor: AppColors.figmaBackground,
      drawer: AgroFenceDrawer(
        propertyName: propertyName,
        currentRoute: AppRouter.properties,
        onPropertySelected: (prop) => Navigator.pushReplacementNamed(
          context,
          AppRouter.home,
          arguments: prop,
        ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            AgroFenceTopBar(
              propertyName: propertyName,
              onMenu: () => _scaffoldKey.currentState?.openDrawer(),
              onPropertySelected: (prop) => Navigator.pushReplacementNamed(
                context,
                AppRouter.home,
                arguments: prop,
              ),
            ),
            Expanded(
              child: RefreshIndicator(
                onRefresh: _load,
                child: ListView(
                  padding: const EdgeInsets.fromLTRB(24, 8, 24, 28),
                  children: [
                    const Text(
                      'Minhas\nPropriedades',
                      style: TextStyle(
                        color: AppColors.figmaPrimary,
                        fontSize: 30,
                        height: 1.14,
                        fontWeight: FontWeight.w800,
                        fontFamily: 'Poppins',
                      ),
                    ),
                    const SizedBox(height: 14),
                    const Text(
                      'Gerencie suas fazendas de forma\nsimples e organizada',
                      style: TextStyle(
                        color: AppColors.figmaMuted,
                        fontSize: 13.5,
                        height: 1.5,
                      ),
                    ),
                    const SizedBox(height: 30),
                    Row(
                      children: [
                        Expanded(
                          child: Container(
                            height: 46,
                            padding: const EdgeInsets.all(4),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(10),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withValues(alpha: .05),
                                  blurRadius: 10,
                                  offset: const Offset(0, 6),
                                ),
                              ],
                            ),
                            child: Row(
                              children: List.generate(
                                3,
                                (i) => Expanded(
                                  child: _FilterTab(
                                    label: const [
                                      'Ativas',
                                      'Inativas',
                                      'Buscar',
                                    ][i],
                                    selected: _filter == i,
                                    onTap: () => setState(() => _filter = i),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(width: 10),
                        Material(
                          color: AppColors.figmaPrimary,
                          borderRadius: BorderRadius.circular(10),
                          child: InkWell(
                            onTap: () async {
                              final created = await Navigator.pushNamed(
                                context,
                                AppRouter.propertyCreate,
                              );
                              if (created == true) _load();
                            },
                            borderRadius: BorderRadius.circular(10),
                            child: const SizedBox(
                              width: 46,
                              height: 46,
                              child: Icon(Icons.add, color: Colors.white),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 28),
                    if (_loading)
                      const SizedBox(
                        height: 260,
                        child: Center(child: CircularProgressIndicator()),
                      )
                    else if (_error != null)
                      _LoadError(message: _error!, onRetry: _load)
                    else if (_properties.isEmpty || _filter == 1)
                      AgroFenceCard(
                        child: Center(
                          child: Padding(
                            padding: const EdgeInsets.all(28),
                            child: Text(
                              _filter == 1
                                  ? 'Nenhuma propriedade inativa'
                                  : 'Cadastre sua primeira propriedade',
                              style: const TextStyle(
                                color: AppColors.figmaMuted,
                              ),
                            ),
                          ),
                        ),
                      )
                    else
                      ..._properties.map(
                        (property) => _PropertyCard(property: property),
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
}

class _FilterTab extends StatelessWidget {
  const _FilterTab({
    required this.label,
    required this.selected,
    required this.onTap,
  });
  final String label;
  final bool selected;
  final VoidCallback onTap;
  @override
  Widget build(BuildContext context) => InkWell(
    onTap: onTap,
    borderRadius: BorderRadius.circular(8),
    child: Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (label != 'Buscar')
              Container(
                width: 6,
                height: 6,
                margin: const EdgeInsets.only(right: 6),
                decoration: BoxDecoration(
                  color: selected
                      ? AppColors.figmaSecondary
                      : Colors.transparent,
                  border: selected
                      ? null
                      : Border.all(color: const Color(0xFFA7B0AB)),
                  borderRadius: BorderRadius.circular(3),
                ),
              ),
            Text(
              label,
              style: TextStyle(
                color: selected ? AppColors.figmaPrimary : AppColors.figmaMuted,
                fontSize: 12,
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
        const SizedBox(height: 8),
        AnimatedContainer(
          duration: const Duration(milliseconds: 180),
          height: 3,
          width: selected ? 90 : 0,
          decoration: BoxDecoration(
            color: AppColors.figmaSecondary,
            borderRadius: BorderRadius.circular(3),
          ),
        ),
      ],
    ),
  );
}

class _PropertyCard extends StatelessWidget {
  const _PropertyCard({required this.property});
  final RegisteredProperty property;
  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 16),
    child: InkWell(
      onTap: () => Navigator.pushReplacementNamed(
        context,
        AppRouter.home,
        arguments: property,
      ),
      borderRadius: BorderRadius.circular(16),
      child: AgroFenceCard(
        child: Stack(
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      width: 66,
                      height: 66,
                      decoration: BoxDecoration(
                        color: const Color(0xFFC9BE8F),
                        borderRadius: BorderRadius.circular(13),
                        gradient: const LinearGradient(
                          colors: [Color(0xFFD5D09C), Color(0xFFA3B78F)],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                      ),
                      child: const Icon(
                        Icons.landscape_rounded,
                        color: AppColors.figmaSecondary,
                      ),
                    ),
                    const SizedBox(width: 14),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            property.name,
                            style: const TextStyle(
                              color: AppColors.figmaPrimary,
                              fontSize: 16,
                              fontWeight: FontWeight.w800,
                              fontFamily: 'Poppins',
                            ),
                          ),
                          const SizedBox(height: 5),
                          Row(
                            children: [
                              const Icon(
                                Icons.location_on,
                                color: Color(0xFFA7B0AB),
                                size: 14,
                              ),
                              const SizedBox(width: 4),
                              Expanded(
                                child: Text(
                                  property.cityState,
                                  style: const TextStyle(
                                    color: AppColors.figmaMuted,
                                    fontSize: 12,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                    const Icon(Icons.more_vert, color: Color(0xFFA7B0AB)),
                  ],
                ),
                const SizedBox(height: 12),
                _Meta(
                  icon: Icons.flag,
                  text: 'Finalidade: ${property.purpose}',
                  muted: true,
                ),
                const _Meta(icon: Icons.pets, text: '— animais'),
                _Meta(
                  icon: Icons.square_foot,
                  text: '${property.hectares.toStringAsFixed(0)} hectares',
                ),
              ],
            ),
            const Positioned(
              bottom: 0,
              right: 0,
              child: CircleAvatar(
                radius: 17,
                backgroundColor: AppColors.figmaSoftGreen,
                child: Icon(
                  Icons.arrow_forward,
                  size: 17,
                  color: AppColors.figmaSecondary,
                ),
              ),
            ),
          ],
        ),
      ),
    ),
  );
}

class _Meta extends StatelessWidget {
  const _Meta({required this.icon, required this.text, this.muted = false});
  final IconData icon;
  final String text;
  final bool muted;
  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 7),
    child: Row(
      children: [
        Icon(
          icon,
          size: 15,
          color: muted ? const Color(0xFFA7B0AB) : AppColors.figmaSecondary,
        ),
        const SizedBox(width: 7),
        Text(
          text,
          style: TextStyle(
            color: muted ? AppColors.figmaMuted : AppColors.figmaText,
            fontSize: 12.5,
            fontWeight: FontWeight.w500,
          ),
        ),
      ],
    ),
  );
}

class _LoadError extends StatelessWidget {
  const _LoadError({required this.message, required this.onRetry});
  final String message;
  final VoidCallback onRetry;
  @override
  Widget build(BuildContext context) => AgroFenceCard(
    child: Column(
      children: [
        const Icon(Icons.cloud_off_rounded, color: Colors.red),
        const SizedBox(height: 8),
        const Text('Não foi possível carregar as propriedades'),
        TextButton(onPressed: onRetry, child: const Text('Tentar novamente')),
      ],
    ),
  );
}

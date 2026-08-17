import 'package:ai_boi/core/di/app_bindings.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/features/animals/data/datasources/animal_remote_data_source.dart';
import 'package:ai_boi/features/animals/domain/entities/animal.dart';
import 'package:ai_boi/features/animals/presentation/pages/animal_detail_page.dart';
import 'package:ai_boi/features/animals/presentation/pages/animal_register_page.dart';
import 'package:flutter/material.dart';

class AnimalsListPage extends StatefulWidget {
  const AnimalsListPage({
    super.key,
    required this.propertyId,
    required this.propertyName,
  });

  final int propertyId;
  final String propertyName;

  @override
  State<AnimalsListPage> createState() => _AnimalsListPageState();
}

class _AnimalsListPageState extends State<AnimalsListPage> {
  late final AnimalRemoteDataSource _dataSource = AppBindings.animalRemote();

  final _searchController = TextEditingController();
  String _searchQuery = '';
  String _categoryFilter = 'Todos';
  int _statusTab = 0;

  List<Animal> _all = [];
  bool _loading = true;
  String? _error;

  static const _categoryFilters = ['Todos', 'Vaca', 'Bezerro', 'Novilha'];

  @override
  void initState() {
    super.initState();
    _load();
    _searchController.addListener(() {
      setState(
        () => _searchQuery = _searchController.text.trim().toLowerCase(),
      );
    });
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final list = await _dataSource.listAnimals(widget.propertyId);
      setState(() {
        _all = list;
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _loading = false;
        _error = e.toString();
      });
    }
  }

  List<Animal> get _filtered {
    var list = _all;

    if (_statusTab == 1) {
      list = list.where((a) => a.isActive).toList();
    } else if (_statusTab == 2) {
      list = list.where((a) => !a.isActive && !a.isDead).toList();
    } else if (_statusTab == 3) {
      list = list.where((a) => a.isDead).toList();
    }

    if (_categoryFilter != 'Todos') {
      list = list.where((a) {
        final cat = a.category.toLowerCase();
        switch (_categoryFilter) {
          case 'Vaca':
            return cat.contains('primípara') ||
                cat.contains('multípara') ||
                cat.contains('vaca');
          case 'Bezerro':
            return cat.contains('bezerro') || cat.contains('bezerra');
          case 'Novilha':
            return cat.contains('novilha') || cat.contains('garrote');
          default:
            return true;
        }
      }).toList();
    }

    if (_searchQuery.isNotEmpty) {
      list = list.where((a) {
        final haystack =
            '${a.displayName} ${a.identificationNumber} ${a.category} ${a.breed ?? ''}'
                .toLowerCase();
        return haystack.contains(_searchQuery);
      }).toList();
    }

    return list;
  }

  Widget _statusBadge(String label, String count, {required bool selected}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          count,
          style: TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 16,
            color: selected ? AppColors.primaryButton : const Color(0xFF1E3A5F),
            fontFamily: 'Poppins',
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: TextStyle(
            fontSize: 12,
            color: selected ? AppColors.primaryButton : AppColors.textSecondary,
            fontFamily: 'Poppins',
          ),
        ),
      ],
    );
  }

  Future<void> _openRegister() async {
    final created = await Navigator.push<bool>(
      context,
      MaterialPageRoute(
        builder: (_) => AnimalRegisterPage(
          propertyName: widget.propertyName,
          propertyId: widget.propertyId,
          dataSource: _dataSource,
        ),
      ),
    );
    if (created == true) _load();
  }

  @override
  Widget build(BuildContext context) {
    final filtered = _filtered;

    return Scaffold(
      backgroundColor: AppColors.backgroundScreen,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        foregroundColor: const Color(0xFF1E3A5F),
        title: const Text(
          'Buscar animais',
          style: TextStyle(
            fontWeight: FontWeight.bold,
            fontFamily: 'Poppins',
            color: Color(0xFF1E3A5F),
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _openRegister,
        backgroundColor: AppColors.primaryButton,
        icon: const Icon(Icons.add, color: Colors.white),
        label: const Text(
          'Novo animal',
          style: TextStyle(color: Colors.white, fontFamily: 'Poppins'),
        ),
      ),
      body: RefreshIndicator(
        onRefresh: _load,
        color: AppColors.primaryButton,
        child: _loading
            ? const Center(child: CircularProgressIndicator())
            : ListView(
                physics: const AlwaysScrollableScrollPhysics(),
                padding: const EdgeInsets.fromLTRB(16, 8, 16, 88),
                children: [
                  TextField(
                    controller: _searchController,
                    enableInteractiveSelection: true,
                    style: const TextStyle(fontFamily: 'Poppins'),
                    decoration: InputDecoration(
                      hintText: 'Buscar por brinco, nome ou identificação...',
                      prefixIcon: const Icon(Icons.search),
                      filled: true,
                      fillColor: Colors.white,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(28),
                        borderSide: BorderSide(color: Colors.grey.shade300),
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(28),
                        borderSide: BorderSide(color: Colors.grey.shade300),
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(16),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withValues(alpha: 0.04),
                          blurRadius: 12,
                          offset: const Offset(0, 2),
                        ),
                      ],
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        _statusBadge(
                          'Todos',
                          _all.length.toString(),
                          selected: _statusTab == 0,
                        ),
                        _statusBadge(
                          'Ativos',
                          _all.where((a) => a.isActive).length.toString(),
                          selected: _statusTab == 1,
                        ),
                        _statusBadge(
                          'Inativos',
                          _all
                              .where((a) => !a.isActive && !a.isDead)
                              .length
                              .toString(),
                          selected: _statusTab == 2,
                        ),
                        _statusBadge(
                          'Óbitos',
                          _all.where((a) => a.isDead).length.toString(),
                          selected: _statusTab == 3,
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    height: 36,
                    child: ListView.separated(
                      scrollDirection: Axis.horizontal,
                      itemCount: _categoryFilters.length,
                      separatorBuilder: (_, _) => const SizedBox(width: 8),
                      itemBuilder: (context, index) {
                        final label = _categoryFilters[index];
                        final selected = _categoryFilter == label;
                        return FilterChip(
                          label: Text(label),
                          selected: selected,
                          onSelected: (_) =>
                              setState(() => _categoryFilter = label),
                          selectedColor: AppColors.primaryButton,
                          labelStyle: TextStyle(
                            color: selected
                                ? Colors.white
                                : AppColors.textPrimary,
                            fontFamily: 'Poppins',
                            fontSize: 12,
                          ),
                          checkmarkColor: Colors.white,
                          backgroundColor: Colors.white,
                          side: BorderSide(
                            color: selected
                                ? AppColors.primaryButton
                                : Colors.grey.shade300,
                          ),
                        );
                      },
                    ),
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      _StatusTab(
                        label: 'Todos',
                        selected: _statusTab == 0,
                        onTap: () => setState(() => _statusTab = 0),
                      ),
                      _StatusTab(
                        label: 'Ativos',
                        selected: _statusTab == 1,
                        onTap: () => setState(() => _statusTab = 1),
                      ),
                      _StatusTab(
                        label: 'Inativos',
                        selected: _statusTab == 2,
                        onTap: () => setState(() => _statusTab = 2),
                      ),
                      _StatusTab(
                        label: 'Óbitos',
                        selected: _statusTab == 3,
                        onTap: () => setState(() => _statusTab = 3),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Text(
                    'Resultados (${filtered.length})',
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 16,
                      color: Color(0xFF1E3A5F),
                      fontFamily: 'Poppins',
                    ),
                  ),
                  if (_error != null) ...[
                    const SizedBox(height: 8),
                    Text(_error!, style: const TextStyle(color: Colors.red)),
                  ],
                  const SizedBox(height: 8),
                  if (filtered.isEmpty)
                    const Padding(
                      padding: EdgeInsets.only(top: 40),
                      child: Center(
                        child: Text(
                          'Nenhum animal encontrado.',
                          style: TextStyle(color: AppColors.textSecondary),
                        ),
                      ),
                    )
                  else
                    ...filtered.map(
                      (animal) => _AnimalTile(
                        animal: animal,
                        onTap: () async {
                          final changed = await Navigator.push<bool>(
                            context,
                            MaterialPageRoute(
                              builder: (_) => AnimalDetailPage(
                                animalId: animal.id,
                                propertyId: widget.propertyId,
                                dataSource: _dataSource,
                              ),
                            ),
                          );
                          if (changed == true) _load();
                        },
                      ),
                    ),
                ],
              ),
      ),
    );
  }
}

class _StatusTab extends StatelessWidget {
  const _StatusTab({
    required this.label,
    required this.selected,
    required this.onTap,
  });

  final String label;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 8),
          decoration: BoxDecoration(
            border: Border(
              bottom: BorderSide(
                color: selected ? AppColors.primaryButton : Colors.transparent,
                width: 2,
              ),
            ),
          ),
          child: Text(
            label,
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: 12,
              fontWeight: selected ? FontWeight.w600 : FontWeight.normal,
              color: selected
                  ? AppColors.primaryButton
                  : AppColors.textSecondary,
              fontFamily: 'Poppins',
            ),
          ),
        ),
      ),
    );
  }
}

class _AnimalTile extends StatelessWidget {
  const _AnimalTile({required this.animal, required this.onTap});

  final Animal animal;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 14),
        decoration: BoxDecoration(
          border: Border(bottom: BorderSide(color: Colors.grey.shade200)),
        ),
        child: Row(
          children: [
            CircleAvatar(
              radius: 24,
              backgroundColor: Colors.grey.shade300,
              child: Icon(
                animal.isFemale ? Icons.female : Icons.male,
                color: AppColors.primaryButton,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Text(
                        animal.displayName,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 16,
                          color: Color(0xFF1E3A5F),
                          fontFamily: 'Poppins',
                        ),
                      ),
                      if (animal.isDead) ...[
                        const SizedBox(width: 8),
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 8,
                            vertical: 2,
                          ),
                          decoration: BoxDecoration(
                            color: Colors.red.shade100,
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: const Text(
                            'Alerta',
                            style: TextStyle(
                              color: Colors.red,
                              fontSize: 10,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ],
                    ],
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'ID - ${animal.identificationNumber} | ${animal.category}',
                    style: const TextStyle(
                      fontSize: 12,
                      color: AppColors.textSecondary,
                      fontFamily: 'Poppins',
                    ),
                  ),
                ],
              ),
            ),
            const Icon(Icons.chevron_right, color: AppColors.textSecondary),
          ],
        ),
      ),
    );
  }
}

import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/labeled_text_field.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/features/animals/data/datasources/animal_remote_data_source.dart';
import 'package:ai_boi/features/animals/data/models/animal_model.dart';
import 'package:ai_boi/features/animals/domain/entities/animal.dart';
import 'package:flutter/material.dart';

class AnimalDetailPage extends StatefulWidget {
  const AnimalDetailPage({
    super.key,
    required this.animalId,
    required this.propertyId,
    required this.dataSource,
  });

  final int animalId;
  final int propertyId;
  final AnimalRemoteDataSource dataSource;

  @override
  State<AnimalDetailPage> createState() => _AnimalDetailPageState();
}

class _AnimalDetailPageState extends State<AnimalDetailPage> {
  Animal? _animal;
  bool _loading = true;
  bool _editing = false;
  bool _saving = false;
  String? _error;

  final _nameController = TextEditingController();
  final _breedController = TextEditingController();
  final _notesController = TextEditingController();
  String? _category;

  static const _categories = [
    'Novilha',
    'Bezerro',
    'Bezerra',
    'Primípara',
    'Multípara',
    'Garrote/Novilho',
    'Touro',
  ];

  @override
  void initState() {
    super.initState();
    _load();
  }

  @override
  void dispose() {
    _nameController.dispose();
    _breedController.dispose();
    _notesController.dispose();
    super.dispose();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final animal = await widget.dataSource.getAnimal(
        widget.animalId,
        widget.propertyId,
      );
      _nameController.text = animal.name ?? '';
      _breedController.text = animal.breed ?? '';
      _notesController.text = animal.notes ?? '';
      _category = animal.category;
      if (!mounted) return;
      setState(() {
        _animal = animal;
        _loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _loading = false;
        _error = e.toString();
      });
    }
  }

  Future<void> _save() async {
    if (_animal == null) return;
    setState(() => _saving = true);
    try {
      final updated = AnimalModel(
        id: _animal!.id,
        identificationNumber: _animal!.identificationNumber,
        name: _nameController.text.trim(),
        sex: _animal!.sex,
        breed: _breedController.text.trim(),
        category: _category ?? _animal!.category,
        lifeStatus: _animal!.lifeStatus,
        reproductiveStatus: _animal!.reproductiveStatus,
        birthDate: _animal!.birthDate,
        origin: _animal!.origin,
        batchId: _animal!.batchId,
        notes: _notesController.text.trim(),
      );
      final result = await widget.dataSource.updateAnimal(
        _animal!.id,
        updated,
        widget.propertyId,
      );
      if (!mounted) return;
      setState(() {
        _animal = result;
        _editing = false;
        _saving = false;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Animal atualizado com sucesso.')),
        );
      }
    } catch (_) {
      if (!mounted) return;
      setState(() => _saving = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Erro ao salvar alterações.'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _registerDeath() async {
    if (_animal == null || _animal!.isDead) return;

    final reasonController = TextEditingController();
    DateTime deathDate = DateTime.now();
    final birthDate = DateTime.tryParse(_animal!.birthDate);
    String deathReason = '';

    final confirmed = await showModalBottomSheet<bool>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) {
        return StatefulBuilder(
          builder: (context, setModalState) {
            return Padding(
              padding: EdgeInsets.only(
                left: 24,
                right: 24,
                top: 24,
                bottom: MediaQuery.of(ctx).viewInsets.bottom + 24,
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Informar morte',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      fontFamily: 'Poppins',
                    ),
                  ),
                  const SizedBox(height: 16),
                  ListTile(
                    contentPadding: EdgeInsets.zero,
                    title: Text(
                      'Data: ${deathDate.day.toString().padLeft(2, '0')}/${deathDate.month.toString().padLeft(2, '0')}/${deathDate.year}',
                    ),
                    trailing: IconButton(
                      icon: const Icon(Icons.calendar_today),
                      onPressed: () async {
                        final picked = await showDatePicker(
                          context: context,
                          initialDate: deathDate,
                          firstDate: birthDate ?? DateTime(1990),
                          lastDate: DateTime.now(),
                        );
                        if (picked != null) {
                          setModalState(() => deathDate = picked);
                        }
                      },
                    ),
                  ),
                  LabeledTextField(
                    label: 'Motivo',
                    hintText: 'Descreva o motivo',
                    controller: reasonController,
                  ),
                  const SizedBox(height: 16),
                  PrimaryButton(
                    text: 'Confirmar óbito',
                    onPressed: () {
                      if (birthDate != null && deathDate.isBefore(birthDate)) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text(
                              'A data de óbito não pode ser anterior ao nascimento.',
                            ),
                            backgroundColor: Colors.red,
                          ),
                        );
                        return;
                      }
                      deathReason = reasonController.text.trim();
                      Navigator.pop(ctx, true);
                    },
                  ),
                ],
              ),
            );
          },
        );
      },
    );

    reasonController.dispose();

    if (confirmed != true || !mounted) return;

    setState(() => _saving = true);
    try {
      final iso =
          '${deathDate.year}-${deathDate.month.toString().padLeft(2, '0')}-${deathDate.day.toString().padLeft(2, '0')}';
      final updated = AnimalModel(
        id: _animal!.id,
        identificationNumber: _animal!.identificationNumber,
        name: _animal!.name,
        sex: _animal!.sex,
        breed: _animal!.breed,
        category: _animal!.category,
        lifeStatus: 'MORTO',
        reproductiveStatus: _animal!.reproductiveStatus,
        birthDate: _animal!.birthDate,
        origin: _animal!.origin,
        batchId: _animal!.batchId,
        notes: 'Óbito em $iso. $deathReason'.trim(),
      );
      final result = await widget.dataSource.updateAnimal(
        _animal!.id,
        updated,
        widget.propertyId,
      );
      if (!mounted) return;
      setState(() {
        _animal = result;
        _saving = false;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Óbito registrado. Inventário atualizado.'),
          ),
        );
        Navigator.pop(context, true);
      }
    } catch (_) {
      if (!mounted) return;
      setState(() => _saving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    if (_error != null || _animal == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('Animal')),
        body: Center(child: Text(_error ?? 'Animal não encontrado')),
      );
    }

    final animal = _animal!;

    return Scaffold(
      backgroundColor: AppColors.backgroundScreen,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        foregroundColor: const Color(0xFF1E3A5F),
        title: Text(
          animal.displayName,
          style: const TextStyle(
            fontWeight: FontWeight.bold,
            fontFamily: 'Poppins',
            color: Color(0xFF1E3A5F),
          ),
        ),
        actions: [
          if (!animal.isDead)
            IconButton(
              icon: Icon(_editing ? Icons.close : Icons.edit),
              onPressed: () => setState(() => _editing = !_editing),
            ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _infoCard(animal),
            if (_editing) ...[
              const SizedBox(height: 16),
              LabeledTextField(
                label: 'Nome',
                hintText: 'Nome',
                controller: _nameController,
              ),
              const SizedBox(height: 12),
              LabeledTextField(
                label: 'Raça',
                hintText: 'Raça',
                controller: _breedController,
              ),
              const SizedBox(height: 12),
              DropdownButtonFormField<String>(
                initialValue: _category,
                decoration: const InputDecoration(labelText: 'Categoria'),
                items: _categories
                    .map((c) => DropdownMenuItem(value: c, child: Text(c)))
                    .toList(),
                onChanged: (v) => setState(() => _category = v),
              ),
              const SizedBox(height: 12),
              LabeledTextField(
                label: 'Observações',
                hintText: 'Observações',
                controller: _notesController,
              ),
              const SizedBox(height: 16),
              PrimaryButton(
                text: _saving ? 'Salvando...' : 'Salvar alterações',
                onPressed: _saving ? null : _save,
              ),
            ],
            if (!animal.isDead) ...[
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                height: PrimaryButton.heightFor(context),
                child: OutlinedButton.icon(
                  onPressed: _saving ? null : _registerDeath,
                  icon: const Icon(Icons.dangerous_outlined, color: Colors.red),
                  label: const Text(
                    'Informar morte',
                    style: TextStyle(color: Colors.red, fontFamily: 'Poppins'),
                  ),
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: Colors.red),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _infoCard(Animal animal) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _row('Brinco', animal.identificationNumber.toString()),
          _row('Sexo', animal.sexLabel),
          _row('Categoria', animal.category),
          _row('Raça', animal.breed ?? '—'),
          _row('Status', animal.lifeStatus),
          _row('Nascimento', animal.birthDate),
          _row('Origem', animal.origin),
          if (animal.reproductiveStatus != null)
            _row('Reprodutivo', animal.reproductiveStatus!),
          if (animal.batchId != null) _row('Lote', '#${animal.batchId}'),
          if (animal.notes != null && animal.notes!.isNotEmpty)
            _row('Observações', animal.notes!),
        ],
      ),
    );
  }

  Widget _row(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 120,
            child: Text(
              label,
              style: const TextStyle(
                color: AppColors.textSecondary,
                fontSize: 13,
              ),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(
                fontWeight: FontWeight.w600,
                fontFamily: 'Poppins',
              ),
            ),
          ),
        ],
      ),
    );
  }
}

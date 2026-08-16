import 'package:flutter/material.dart';
import 'package:ai_boi/core/di/app_bindings.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/labeled_text_field.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/features/animals/data/models/animal_model.dart';

String _todayPtBr() {
  final today = DateTime.now();
  final day = today.day.toString().padLeft(2, '0');
  final month = today.month.toString().padLeft(2, '0');
  return '$day/$month/${today.year}';
}

class DeathReportPage extends StatefulWidget {
  const DeathReportPage({
    super.key,
    required this.propertyId,
    required this.propertyName,
  });

  final int propertyId;
  final String propertyName;

  @override
  State<DeathReportPage> createState() => _DeathReportPageState();
}

class _DeathReportPageState extends State<DeathReportPage> {
  final _formKey = GlobalKey<FormState>();
  final _causeController = TextEditingController();

  List<AnimalModel> _animals = [];
  AnimalModel? _selectedAnimal;
  bool _loadingAnimals = true;
  bool _submitting = false;

  @override
  void initState() {
    super.initState();
    _loadAnimals();
  }

  Future<void> _loadAnimals() async {
    try {
      final animals = await AppBindings.animalRemote().listAnimals(
        widget.propertyId,
      );
      if (!mounted) return;
      setState(() {
        // Filtrar apenas ativos
        _animals = animals
            .where((animal) => animal.lifeStatus.toUpperCase() == 'ATIVO')
            .toList();
        _loadingAnimals = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() => _loadingAnimals = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Erro ao carregar animais: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  Future<void> _submitDeathReport() async {
    if (_selectedAnimal == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Selecione um animal'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }
    if (!_formKey.currentState!.validate()) return;

    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text(
          'Confirmar Registro de Óbito',
          style: TextStyle(fontWeight: FontWeight.bold, fontFamily: 'Poppins'),
        ),
        content: Text(
          'Tem certeza que deseja marcar o animal de brinco ${_selectedAnimal!.identificationNumber} como morto? Esta ação alterará seu status permanentemente.',
          style: const TextStyle(fontFamily: 'Poppins'),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancelar', style: TextStyle(color: Colors.grey)),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text(
              'Confirmar',
              style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold),
            ),
          ),
        ],
      ),
    );

    if (confirm != true) return;

    setState(() => _submitting = true);
    try {
      // 1. Atualizar o status do animal
      final updatedAnimal = AnimalModel(
        id: _selectedAnimal!.id,
        identificationNumber: _selectedAnimal!.identificationNumber,
        name: _selectedAnimal!.name,
        sex: _selectedAnimal!.sex,
        breed: _selectedAnimal!.breed,
        category: _selectedAnimal!.category,
        lifeStatus: 'MORTO',
        reproductiveStatus: _selectedAnimal!.reproductiveStatus,
        birthDate: _selectedAnimal!.birthDate,
        origin: _selectedAnimal!.origin,
        batchId: _selectedAnimal!.batchId,
        notes:
            '${_selectedAnimal!.notes ?? ""}\nÓbito em: ${_todayPtBr()} | Motivo: ${_causeController.text.trim()}',
        birthWeight: _selectedAnimal!.birthWeight,
        weaningWeight: _selectedAnimal!.weaningWeight,
        entryDate: _selectedAnimal!.entryDate,
        pedigreePo: _selectedAnimal!.pedigreePo,
      );
      await AppBindings.animalRemote().updateAnimal(
        _selectedAnimal!.id,
        updatedAnimal,
        widget.propertyId,
      );

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Óbito registrado com sucesso!'),
          backgroundColor: Colors.green,
        ),
      );
      _causeController.clear();
      if (!mounted) return;
      setState(() {
        _selectedAnimal = null;
      });
      _loadAnimals(); // Recarregar lista
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Erro ao registrar óbito: $e'),
          backgroundColor: Colors.red,
        ),
      );
    } finally {
      if (!mounted) return;
      setState(() => _submitting = false);
    }
  }

  @override
  void dispose() {
    _causeController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: AppColors.primaryButton,
        foregroundColor: Colors.white,
        title: const Text(
          'Registrar Óbito',
          style: TextStyle(fontWeight: FontWeight.bold, fontFamily: 'Poppins'),
        ),
      ),
      body: _loadingAnimals
          ? const Center(
              child: CircularProgressIndicator(color: AppColors.primaryGreen),
            )
          : SingleChildScrollView(
              padding: const EdgeInsets.all(24.0),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Selecione o Animal',
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                        color: AppColors.textPrimary,
                        fontFamily: 'Poppins',
                      ),
                    ),
                    const SizedBox(height: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      decoration: BoxDecoration(
                        border: Border.all(color: Colors.grey.shade300),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: DropdownButtonHideUnderline(
                        child: DropdownButton<AnimalModel>(
                          value: _selectedAnimal,
                          hint: const Text(
                            'Escolha o brinco/ID do animal',
                            style: TextStyle(fontFamily: 'Poppins'),
                          ),
                          isExpanded: true,
                          onChanged: (AnimalModel? value) {
                            setState(() => _selectedAnimal = value);
                          },
                          items: _animals.map((AnimalModel animal) {
                            return DropdownMenuItem<AnimalModel>(
                              value: animal,
                              child: Text(
                                'Brinco: ${animal.identificationNumber} - ${animal.name ?? "Sem nome"}',
                                style: const TextStyle(fontFamily: 'Poppins'),
                              ),
                            );
                          }).toList(),
                        ),
                      ),
                    ),
                    const SizedBox(height: 20),
                    LabeledTextField(
                      label: 'Causa da Morte / Observações',
                      hintText: 'Ex: Picada de cobra / Acidente (Opcional)',
                      controller: _causeController,
                    ),
                    const SizedBox(height: 32),
                    PrimaryButton(
                      text: _submitting ? 'Enviando...' : 'Confirmar Óbito',
                      onPressed: _submitting ? null : _submitDeathReport,
                    ),
                  ],
                ),
              ),
            ),
    );
  }
}

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

class ReproductionPage extends StatefulWidget {
  const ReproductionPage({
    super.key,
    required this.propertyId,
    required this.propertyName,
  });

  final int propertyId;
  final String propertyName;

  @override
  State<ReproductionPage> createState() => _ReproductionPageState();
}

class _ReproductionPageState extends State<ReproductionPage> {
  final _formKey = GlobalKey<FormState>();
  final _notesController = TextEditingController();

  List<AnimalModel> _femaleAnimals = [];
  AnimalModel? _selectedAnimal;
  String _reproductionType = 'MONTA_NATURAL';
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
        // Filtrar apenas fêmeas
        _femaleAnimals = animals
            .where((animal) => animal.sex.toUpperCase() == 'F')
            .toList();
        _loadingAnimals = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() => _loadingAnimals = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Erro ao carregar matrizes: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  Future<void> _submitReproduction() async {
    if (_selectedAnimal == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Selecione uma matriz'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }
    if (!_formKey.currentState!.validate()) return;

    setState(() => _submitting = true);
    try {
      await AppBindings.operations().createReproduction(widget.propertyId, {
        'reproduction_type': _reproductionType,
        'reproduction_status': 'IN_PROGRESS',
        'start_date': _todayPtBr(),
        'notes': _notesController.text.trim().isEmpty
            ? null
            : _notesController.text.trim(),
        'animal_id': _selectedAnimal!.id,
      });

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Ciclo reprodutivo iniciado com sucesso!'),
          backgroundColor: Colors.green,
        ),
      );
      _notesController.clear();
      if (!mounted) return;
      setState(() {
        _selectedAnimal = null;
        _submitting = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() => _submitting = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Erro ao registrar ciclo reprodutivo: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  void dispose() {
    _notesController.dispose();
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
          'Módulo de Reprodução',
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
                      'Selecione a Matriz (Fêmea)',
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
                            'Escolha o brinco/ID da fêmea',
                            style: TextStyle(fontFamily: 'Poppins'),
                          ),
                          isExpanded: true,
                          onChanged: (AnimalModel? value) {
                            setState(() => _selectedAnimal = value);
                          },
                          items: _femaleAnimals.map((AnimalModel animal) {
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
                    const Text(
                      'Tipo de Protocolo',
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
                        child: DropdownButton<String>(
                          value: _reproductionType,
                          isExpanded: true,
                          onChanged: (String? value) {
                            if (value != null) {
                              setState(() => _reproductionType = value);
                            }
                          },
                          items: const [
                            DropdownMenuItem(
                              value: 'MONTA_NATURAL',
                              child: Text(
                                'Monta Natural',
                                style: TextStyle(fontFamily: 'Poppins'),
                              ),
                            ),
                            DropdownMenuItem(
                              value: 'IATF',
                              child: Text(
                                'IATF (Inseminação em Tempo Fixo)',
                                style: TextStyle(fontFamily: 'Poppins'),
                              ),
                            ),
                            DropdownMenuItem(
                              value: 'TE',
                              child: Text(
                                'Transferência de Embrião (TE)',
                                style: TextStyle(fontFamily: 'Poppins'),
                              ),
                            ),
                            DropdownMenuItem(
                              value: 'FIV',
                              child: Text(
                                'Fertilização In Vitro (FIV)',
                                style: TextStyle(fontFamily: 'Poppins'),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 20),
                    LabeledTextField(
                      label: 'Observações / Notas',
                      hintText:
                          'Digite alguma observação sobre o início do ciclo (Opcional)',
                      controller: _notesController,
                    ),
                    const SizedBox(height: 32),
                    PrimaryButton(
                      text: _submitting
                          ? 'Enviando...'
                          : 'Iniciar Ciclo Reprodutivo',
                      onPressed: _submitting ? null : _submitReproduction,
                    ),
                  ],
                ),
              ),
            ),
    );
  }
}

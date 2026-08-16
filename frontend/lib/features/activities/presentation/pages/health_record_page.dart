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

class HealthRecordPage extends StatefulWidget {
  const HealthRecordPage({
    super.key,
    required this.propertyId,
    required this.propertyName,
  });

  final int propertyId;
  final String propertyName;

  @override
  State<HealthRecordPage> createState() => _HealthRecordPageState();
}

class _HealthRecordPageState extends State<HealthRecordPage> {
  final _formKey = GlobalKey<FormState>();
  final _productController = TextEditingController();
  final _responsibleController = TextEditingController();
  final _dosageController = TextEditingController();
  final _notesController = TextEditingController();

  List<AnimalModel> _animals = [];
  AnimalModel? _selectedAnimal;
  String _treatmentType = 'VACCINE';
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
        _animals = animals;
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

  Future<void> _submitHealthRecord() async {
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

    setState(() => _submitting = true);
    try {
      final dosageVal = double.tryParse(_dosageController.text);
      await AppBindings.operations().createHealthRecord({
        'health_type': _treatmentType,
        'product_name': _productController.text.trim(),
        'responsible': _responsibleController.text.trim(),
        'application_date': _todayPtBr(),
        'dosage': dosageVal,
        'notes': _notesController.text.trim().isEmpty
            ? null
            : _notesController.text.trim(),
        'property_id': widget.propertyId,
        'animal_id': _selectedAnimal!.id,
      }, propertyId: widget.propertyId);

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Registro de saúde salvo com sucesso!'),
          backgroundColor: Colors.green,
        ),
      );
      _productController.clear();
      _responsibleController.clear();
      _dosageController.clear();
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
          content: Text('Erro ao registrar manejo sanitário: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  void dispose() {
    _productController.dispose();
    _responsibleController.dispose();
    _dosageController.dispose();
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
          'Manejo Sanitário',
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
                    const Text(
                      'Tipo de Tratamento',
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
                          value: _treatmentType,
                          isExpanded: true,
                          onChanged: (String? value) {
                            if (value != null) {
                              setState(() => _treatmentType = value);
                            }
                          },
                          items: const [
                            DropdownMenuItem(
                              value: 'VACCINE',
                              child: Text(
                                'Vacina',
                                style: TextStyle(fontFamily: 'Poppins'),
                              ),
                            ),
                            DropdownMenuItem(
                              value: 'MEDICATION',
                              child: Text(
                                'Tratamento / Medicamento',
                                style: TextStyle(fontFamily: 'Poppins'),
                              ),
                            ),
                            DropdownMenuItem(
                              value: 'DEWORMER',
                              child: Text(
                                'Desverminação',
                                style: TextStyle(fontFamily: 'Poppins'),
                              ),
                            ),
                            DropdownMenuItem(
                              value: 'EXAM',
                              child: Text(
                                'Exame / Diagnóstico',
                                style: TextStyle(fontFamily: 'Poppins'),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 20),
                    LabeledTextField(
                      label: 'Nome do Produto',
                      hintText: 'Ex: Vacina Contra Aftosa',
                      controller: _productController,
                      validator: (v) => v == null || v.trim().isEmpty
                          ? 'Informe o nome do produto'
                          : null,
                    ),
                    const SizedBox(height: 20),
                    LabeledTextField(
                      label: 'Responsável',
                      hintText: 'Ex: Dr. Carlos Silva',
                      controller: _responsibleController,
                      validator: (v) => v == null || v.trim().isEmpty
                          ? 'Informe o responsável'
                          : null,
                    ),
                    const SizedBox(height: 20),
                    LabeledTextField(
                      label: 'Dosagem (ml / doses)',
                      hintText: 'Ex: 2.0 (Opcional)',
                      controller: _dosageController,
                      keyboardType: const TextInputType.numberWithOptions(
                        decimal: true,
                      ),
                    ),
                    const SizedBox(height: 20),
                    LabeledTextField(
                      label: 'Observações / Notas',
                      hintText: 'Digite alguma informação relevante (Opcional)',
                      controller: _notesController,
                    ),
                    const SizedBox(height: 32),
                    PrimaryButton(
                      text: _submitting
                          ? 'Enviando...'
                          : 'Salvar Registro Sanitário',
                      onPressed: _submitting ? null : _submitHealthRecord,
                    ),
                  ],
                ),
              ),
            ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:ai_boi/core/di/app_bindings.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/labeled_text_field.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/features/animals/data/models/animal_model.dart';

class WeighingPage extends StatefulWidget {
  const WeighingPage({
    super.key,
    required this.propertyId,
    required this.propertyName,
  });

  final int propertyId;
  final String propertyName;

  @override
  State<WeighingPage> createState() => _WeighingPageState();
}

class _WeighingPageState extends State<WeighingPage> {
  final _formKey = GlobalKey<FormState>();
  final _weightController = TextEditingController();

  List<AnimalModel> _animals = [];
  AnimalModel? _selectedAnimal;
  bool _loadingAnimals = true;
  bool _submitting = false;

  @override
  void initState() {
    super.initState();
    _loadAnimals();
  }

  String _formatDate(DateTime dt) {
    final y = dt.year.toString().padLeft(4, '0');
    final m = dt.month.toString().padLeft(2, '0');
    final d = dt.day.toString().padLeft(2, '0');
    return '$d/$m/$y';
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

  Future<void> _submitWeighing() async {
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
      final weight = double.tryParse(_weightController.text) ?? 0.0;
      await AppBindings.operations().createWeighing({
        'weight': weight,
        'animal_id': _selectedAnimal!.id,
        'weigh_date': _formatDate(DateTime.now()),
      }, propertyId: widget.propertyId);

      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Pesagem registrada com sucesso!'),
          backgroundColor: Colors.green,
        ),
      );
      _weightController.clear();
      setState(() {
        _selectedAnimal = null;
        _submitting = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() => _submitting = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Erro ao registrar pesagem: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  void dispose() {
    _weightController.dispose();
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
          'Registrar Pesagem',
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
                    const SizedBox(height: 24),
                    LabeledTextField(
                      label: 'Peso (Kg)',
                      hintText: 'Ex: 450.5',
                      controller: _weightController,
                      keyboardType: const TextInputType.numberWithOptions(
                        decimal: true,
                      ),
                      validator: (v) {
                        if (v == null || v.isEmpty) return 'Informe o peso';
                        if (double.tryParse(v) == null) return 'Peso inválido';
                        return null;
                      },
                    ),
                    const SizedBox(height: 32),
                    PrimaryButton(
                      text: _submitting ? 'Enviando...' : 'Salvar Pesagem',
                      onPressed: _submitting ? null : _submitWeighing,
                    ),
                  ],
                ),
              ),
            ),
    );
  }
}

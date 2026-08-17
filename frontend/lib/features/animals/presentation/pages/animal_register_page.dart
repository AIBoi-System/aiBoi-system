import 'package:flutter/material.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/features/animals/data/datasources/animal_remote_data_source.dart';
import 'package:ai_boi/features/animals/data/models/animal_model.dart';
import 'package:ai_boi/features/animals/presentation/widgets/animal_step_header.dart';
import 'package:intl/intl.dart';

import 'steps/animal_form_data.dart';
import 'steps/animal_register_step_1_identification.dart';
import 'steps/animal_register_step_2_category.dart';
import 'steps/animal_register_step_3_dates.dart';
import 'steps/animal_register_step_4_location.dart';
import 'steps/animal_register_step_5_genealogy.dart';
import 'steps/animal_register_step_6_development.dart';
import 'steps/animal_register_step_7_health.dart';
import 'steps/animal_register_step_8_summary.dart';

class AnimalRegisterPage extends StatefulWidget {
  const AnimalRegisterPage({
    super.key,
    required this.propertyName,
    required this.propertyId,
    required this.dataSource,
  });

  final String propertyName;
  final int propertyId;
  final AnimalRemoteDataSource dataSource;

  @override
  State<AnimalRegisterPage> createState() => _AnimalRegisterPageState();
}

class _AnimalRegisterPageState extends State<AnimalRegisterPage> {
  final _pageController = PageController();
  int _step = 1;
  bool _submitting = false;

  final _formData = AnimalFormData();

  // One key per form step that requires validation
  final _formKeys = List.generate(8, (_) => GlobalKey<FormState>());

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  bool _validateStep(int stepIndex) {
    if (stepIndex == 8) return true; // Summary has no inputs to validate
    final key = _formKeys[stepIndex - 1];
    if (key.currentState != null) {
      return key.currentState!.validate();
    }
    return true; // Default true if no form key or not built yet
  }

  void _next() {
    if (!_validateStep(_step)) return;

    if (_step < 8) {
      setState(() => _step++);
      _pageController.nextPage(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
    } else {
      _submit();
    }
  }

  void _back() {
    if (_step > 1) {
      setState(() => _step--);
      _pageController.previousPage(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
    } else {
      Navigator.pop(context);
    }
  }

  String _isoDate(DateTime d) =>
      '${d.year.toString().padLeft(4, '0')}-${d.month.toString().padLeft(2, '0')}-${d.day.toString().padLeft(2, '0')}';

  Future<void> _submit() async {
    setState(() => _submitting = true);
    try {
      final category = _formData.categoria ?? (_formData.sexo == 'F' ? 'Vaca' : 'Touro');
      final origin = _formData.origem ?? 'PROPRIEDADE';
      final birthDate = _formData.dataNascimento ?? DateTime.now();

      final animal = AnimalModel(
        id: 0,
        identificationNumber: _formData.brinco ?? 0,
        name: _formData.nome?.trim().isEmpty ?? true ? null : _formData.nome?.trim(),
        sex: _formData.sexo,
        breed: _formData.raca?.trim().isEmpty ?? true ? null : _formData.raca?.trim(),
        category: category,
        lifeStatus: _formData.statusAnimal?.toUpperCase() ?? 'ATIVO',
        reproductiveStatus: _formData.sexo == 'F' ? _formData.statusReprodutivo : null,
        birthDate: _isoDate(birthDate),
        origin: origin,
        batchId: _formData.loteId,
        notes: _formData.notas?.trim().isEmpty ?? true ? null : _formData.notas?.trim(),
        birthWeight: _formData.pesoNascer,
        weaningWeight: _formData.pesoAtual,
        entryDate: _formData.dataEntrada != null ? _isoDate(_formData.dataEntrada!) : null,
        pedigreePo: _formData.pedigreePo,
      );

      await widget.dataSource.createAnimal(animal, widget.propertyId);

      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Animal cadastrado com sucesso!'),
          backgroundColor: AppColors.primaryButton,
        ),
      );
      Navigator.pop(context, true);
    } catch (e) {
      if (!mounted) return;
      final msg = e.toString();
      if (msg.contains('já existe') || msg.contains('400')) {
        _showError('Este brinco já está cadastrado na propriedade.');
      } else {
        _showError('Erro ao cadastrar animal. Verifique os dados.');
      }
    } finally {
      if (mounted) setState(() => _submitting = false);
    }
  }

  void _showError(String msg) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(msg), backgroundColor: Colors.red),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.backgroundScreen,
      appBar: AppBar(
        backgroundColor: AppColors.backgroundScreen,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: _back,
        ),
        title: const Text(
          'Cadastrar Animal',
          style: TextStyle(
            color: Colors.black,
            fontSize: 16,
            fontWeight: FontWeight.w700,
            fontFamily: 'Poppins',
          ),
        ),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
            child: AnimalStepHeader(currentStep: _step, totalSteps: 8),
          ),
          Expanded(
            child: PageView(
              controller: _pageController,
              physics: const NeverScrollableScrollPhysics(),
              children: [
                AnimalRegisterStep1Identification(
                    formData: _formData, formKey: _formKeys[0]),
                AnimalRegisterStep2Category(
                    formData: _formData, formKey: _formKeys[1]),
                AnimalRegisterStep3Dates(
                    formData: _formData, formKey: _formKeys[2]),
                AnimalRegisterStep4Location(
                    formData: _formData,
                    formKey: _formKeys[3],
                    dataSource: widget.dataSource),
                AnimalRegisterStep5Genealogy(
                    formData: _formData, formKey: _formKeys[4]),
                AnimalRegisterStep6Development(
                    formData: _formData, formKey: _formKeys[5]),
                AnimalRegisterStep7Health(
                    formData: _formData, formKey: _formKeys[6]),
                AnimalRegisterStep8Summary(formData: _formData),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.all(24),
            decoration: const BoxDecoration(
              color: Colors.white,
              border: Border(top: BorderSide(color: Color(0xFFEEEEEE))),
            ),
            child: PrimaryButton(
              text: _step == 8 ? 'Finalizar Cadastro' : 'Avançar',
              isLoading: _submitting,
              onPressed: _next,
            ),
          ),
        ],
      ),
    );
  }
}

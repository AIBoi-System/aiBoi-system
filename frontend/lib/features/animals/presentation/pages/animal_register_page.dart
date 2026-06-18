import 'dart:ui';

import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/labeled_text_field.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/features/animals/data/datasources/animal_remote_data_source.dart';
import 'package:ai_boi/features/animals/data/models/animal_model.dart';
import 'package:ai_boi/features/animals/presentation/widgets/animal_step_header.dart';
import 'package:flutter/material.dart';

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

  final _brincoController = TextEditingController();
  final _nameController = TextEditingController();
  final _breedController = TextEditingController();
  final _notesController = TextEditingController();
  final _birthWeightController = TextEditingController();
  final _currentWeightController = TextEditingController();
  final _pedigreeController = TextEditingController();
  final _fatherController = TextEditingController();
  final _motherController = TextEditingController();
  final _paternalGrandfatherController = TextEditingController();
  final _paternalGrandmotherController = TextEditingController();
  final _maternalGrandfatherController = TextEditingController();
  final _maternalGrandmotherController = TextEditingController();

  String _sex = 'F';
  String? _category;
  String? _reproductiveStatus;
  String? _origin;
  DateTime? _birthDate;
  DateTime? _entryDate;
  int? _batchId;
  String? _pasture;
  String? _productionSystem;
  String? _animalStatus;
  String? _condition;
  bool _hasGenealogy = false;
  bool _quickRegister = false;

  List<Map<String, dynamic>> _batches = [];

  static const _categories = [
    'Novilha',
    'Bezerro',
    'Bezerra',
    'Primípara',
    'Multípara',
    'Garrote/Novilho',
    'Touro',
  ];

  static const _reproductiveStatuses = ['MVAZIO', 'PRENHE', 'FAPTO_MONTA'];

  static const _origins = ['PROPRIEDADE', 'COMPRA', 'TRANSFERENCIA'];

  static const _productionSystems = ['Cria', 'Recria', 'Engorda', 'Leite'];

  static const _animalStatusOptions = ['Ativo', 'Inativo', 'Morto'];

  static const _conditionOptions = ['Magro', 'Ideal', 'Gordo'];

  @override
  void initState() {
    super.initState();
    _loadBatches();
  }

  Future<void> _loadBatches() async {
    try {
      final batches = await widget.dataSource.listBatches();
      if (mounted) setState(() => _batches = batches.cast<Map<String, dynamic>>());
    } catch (_) {}
  }

  @override
  void dispose() {
    _pageController.dispose();
    _brincoController.dispose();
    _nameController.dispose();
    _breedController.dispose();
    _notesController.dispose();
    _birthWeightController.dispose();
    _currentWeightController.dispose();
    _pedigreeController.dispose();
    _fatherController.dispose();
    _motherController.dispose();
    _paternalGrandfatherController.dispose();
    _paternalGrandmotherController.dispose();
    _maternalGrandfatherController.dispose();
    _maternalGrandmotherController.dispose();
    super.dispose();
  }

  Future<void> _pickDate({
    required ValueChanged<DateTime> onPicked,
    DateTime? initial,
    DateTime? lastDate,
  }) async {
    final picked = await showDatePicker(
      context: context,
      initialDate: initial ?? DateTime.now(),
      firstDate: DateTime(1990),
      lastDate: lastDate ?? DateTime.now(),
    );
    if (picked != null) onPicked(picked);
  }

  String _isoDate(DateTime d) =>
      '${d.year.toString().padLeft(4, '0')}-${d.month.toString().padLeft(2, '0')}-${d.day.toString().padLeft(2, '0')}';

  String _ageText() {
    if (_birthDate == null) return '-';
    final now = DateTime.now();
    var years = now.year - _birthDate!.year;
    if (now.month < _birthDate!.month ||
        (now.month == _birthDate!.month && now.day < _birthDate!.day)) {
      years--;
    }
    if (years < 0) return '-';
    if (years == 0) return 'Menos de 1 ano';
    return '$years ano${years == 1 ? '' : 's'}';
  }

  bool _validateStep(int step) {
    switch (step) {
      case 1:
        if (_brincoController.text.trim().isEmpty) {
          _showError('Informe o número do brinco.');
          return false;
        }
        if (_batchId == null) {
          _showError('Selecione o lote.');
          return false;
        }
        if (!_quickRegister) {
          if (_category == null) {
            _showError('Selecione a categoria.');
            return false;
          }
          if (_birthDate == null) {
            _showError('Selecione a data de nascimento.');
            return false;
          }
          if (_origin == null) {
            _showError('Selecione a origem.');
            return false;
          }
          if (_sex == 'F' && _reproductiveStatus == null) {
            _showError('Informe o status reprodutivo da fêmea.');
            return false;
          }
        }
        return true;
      default:
        return true;
    }
  }

  void _showError(String msg) {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(SnackBar(content: Text(msg), backgroundColor: Colors.red));
  }

  void _next() {
    if (!_validateStep(_step)) return;
    if (_step < 5) {
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

  Future<void> _submit() async {
    setState(() => _submitting = true);
    try {
      final brinco = int.parse(_brincoController.text.trim());
      final category = _category ?? (_sex == 'F' ? 'Vaca' : 'Touro');
      final origin = _origin ?? 'PROPRIEDADE';
      final birthDate = _birthDate ?? DateTime.now();
      final animal = AnimalModel(
        id: 0,
        identificationNumber: brinco,
        name: _nameController.text.trim().isEmpty
            ? null
            : _nameController.text.trim(),
        sex: _sex,
        breed: _breedController.text.trim().isEmpty
            ? null
            : _breedController.text.trim(),
        category: category,
        lifeStatus: _animalStatus?.toUpperCase() ?? 'ATIVO',
        reproductiveStatus: _sex == 'F' ? _reproductiveStatus : null,
        birthDate: _isoDate(birthDate),
        origin: origin,
        batchId: _batchId,
        notes: _notesController.text.trim().isEmpty
            ? null
            : _notesController.text.trim(),
        birthWeight: double.tryParse(
          _birthWeightController.text.replaceAll(',', '.'),
        ),
        weaningWeight: double.tryParse(
          _currentWeightController.text.replaceAll(',', '.'),
        ),
        entryDate: _entryDate != null ? _isoDate(_entryDate!) : null,
        pedigreePo: _hasGenealogy
            ? int.tryParse(_pedigreeController.text.trim())
            : null,
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
            child: AnimalStepHeader(currentStep: _step),
          ),
          Expanded(
            child: PageView(
              controller: _pageController,
              physics: const NeverScrollableScrollPhysics(),
              children: [_step1(), _step2(), _step3(), _step4(), _step5()],
            ),
          ),
          _footer(),
        ],
      ),
    );
  }

  Widget _card({required String title, required Widget child, IconData? icon}) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(16),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
        child: Container(
          margin: const EdgeInsets.all(16),
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: Colors.white.withValues(alpha: 0.82),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: Colors.white.withValues(alpha: 0.65)),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.08),
                blurRadius: 18,
                offset: const Offset(0, 8),
              ),
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  if (icon != null) ...[
                    Icon(icon, color: AppColors.primaryButton, size: 20),
                    const SizedBox(width: 8),
                  ],
                  Text(
                    title,
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 16,
                      fontFamily: 'Poppins',
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              child,
            ],
          ),
        ),
      ),
    );
  }

  Widget _step1() {
    return SingleChildScrollView(
      child: _card(
        title: 'Identificação do Animal',
        icon: Icons.pets,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Informe os dados do animal',
              style: TextStyle(
                fontSize: 14,
                color: AppColors.textSecondary,
                fontFamily: 'Poppins',
              ),
            ),
            const SizedBox(height: 20),
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 120,
                  height: 140,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: Colors.grey.shade300, width: 1.5),
                    color: Colors.white,
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(
                        Icons.camera_alt_outlined,
                        size: 36,
                        color: Colors.grey,
                      ),
                      const SizedBox(height: 12),
                      const Text(
                        'Adicionar foto',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: Colors.grey,
                          fontFamily: 'Poppins',
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                      const SizedBox(height: 4),
                      const Text(
                        'jpg, png até 5MB',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: Colors.grey,
                          fontSize: 12,
                          fontFamily: 'Poppins',
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    children: [
                      LabeledTextField(
                        label: 'Nº do Brinco',
                        hintText: 'Ex: 12345, ABC123',
                        controller: _brincoController,
                        keyboardType: TextInputType.number,
                      ),
                      const SizedBox(height: 16),
                      LabeledTextField(
                        label: 'Nome',
                        hintText: 'Ex: Estrela',
                        controller: _nameController,
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),
            const Text('Sexo', style: TextStyle(fontWeight: FontWeight.w500)),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(
                  child: _SexToggle(
                    label: 'Fêmea',
                    icon: Icons.female,
                    selected: _sex == 'F',
                    onTap: () => setState(() {
                      _sex = 'F';
                      _reproductiveStatus ??= 'MVAZIO';
                    }),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _SexToggle(
                    label: 'Macho',
                    icon: Icons.male,
                    selected: _sex == 'M',
                    onTap: () => setState(() {
                      _sex = 'M';
                      _reproductiveStatus = null;
                    }),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: DropdownButtonFormField<String>(
                    initialValue: _category,
                    decoration: InputDecoration(
                      hintText: 'Selecione',
                      filled: true,
                      fillColor: Colors.white,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: BorderSide(color: Colors.grey.shade300),
                      ),
                    ),
                    items: _categories
                        .map(
                          (value) => DropdownMenuItem(
                            value: value,
                            child: Text(
                              value,
                              style: const TextStyle(fontFamily: 'Poppins'),
                            ),
                          ),
                        )
                        .toList(),
                    onChanged: (value) => setState(() => _category = value),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: LabeledTextField(
                    label: 'Raça',
                    hintText: 'Selecione',
                    controller: _breedController,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<int>(
              initialValue: _batchId,
              decoration: InputDecoration(
                labelText: 'Lote',
                filled: true,
                fillColor: Colors.white,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide(color: Colors.grey.shade300),
                ),
              ),
              items: _batches.map((batch) {
                final batchId = batch['id_batch'] ?? batch['id'];
                final value = batchId is int
                    ? batchId
                    : int.tryParse(batchId?.toString() ?? '');
                return DropdownMenuItem<int>(
                  value: value,
                  child: Text(
                    batch['name']?.toString() ?? 'Lote',
                    style: const TextStyle(fontFamily: 'Poppins'),
                  ),
                );
              }).toList(),
              onChanged: (value) => setState(() => _batchId = value),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Data de Nascimento',
                        style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w500,
                          color: AppColors.textPrimary,
                          fontFamily: 'Poppins',
                        ),
                      ),
                      const SizedBox(height: 8),
                      InkWell(
                        borderRadius: BorderRadius.circular(12),
                        onTap: () => _pickDate(
                          initial: _birthDate,
                          onPicked: (value) =>
                              setState(() => _birthDate = value),
                        ),
                        child: Container(
                          height: 48,
                          padding: const EdgeInsets.symmetric(horizontal: 16),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(color: Colors.grey.shade300),
                          ),
                          alignment: Alignment.centerLeft,
                          child: Text(
                            _birthDate == null
                                ? 'Selecione a data'
                                : _isoDate(_birthDate!),
                            style: TextStyle(
                              color: _birthDate == null
                                  ? AppColors.textSecondary
                                  : Colors.black,
                              fontFamily: 'Poppins',
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Idade',
                        style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w500,
                          color: AppColors.textPrimary,
                          fontFamily: 'Poppins',
                        ),
                      ),
                      const SizedBox(height: 8),
                      Container(
                        height: 48,
                        padding: const EdgeInsets.symmetric(horizontal: 16),
                        alignment: Alignment.centerLeft,
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: Colors.grey.shade300),
                        ),
                        child: Text(
                          _ageText(),
                          style: const TextStyle(
                            fontFamily: 'Poppins',
                            color: AppColors.textSecondary,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppColors.primaryButton.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                children: const [
                  Icon(Icons.lightbulb, color: AppColors.primaryButton),
                  SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      'Dica: a idade será calculada automaticamente',
                      style: TextStyle(
                        fontFamily: 'Poppins',
                        color: AppColors.textSecondary,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: DropdownButtonFormField<String>(
                    initialValue: _reproductiveStatus,
                    decoration: InputDecoration(
                      hintText: 'Selecione',
                      filled: true,
                      fillColor: Colors.white,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: BorderSide(color: Colors.grey.shade300),
                      ),
                    ),
                    items: _reproductiveStatuses
                        .map(
                          (value) => DropdownMenuItem(
                            value: value,
                            child: Text(
                              value,
                              style: const TextStyle(fontFamily: 'Poppins'),
                            ),
                          ),
                        )
                        .toList(),
                    onChanged: _sex == 'F'
                        ? (value) => setState(() => _reproductiveStatus = value)
                        : null,
                    disabledHint: const Text(
                      'Selecione',
                      style: TextStyle(fontFamily: 'Poppins'),
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: DropdownButtonFormField<String>(
                    initialValue: _origin,
                    decoration: InputDecoration(
                      hintText: 'Selecione',
                      filled: true,
                      fillColor: Colors.white,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: BorderSide(color: Colors.grey.shade300),
                      ),
                    ),
                    items: _origins
                        .map(
                          (value) => DropdownMenuItem(
                            value: value,
                            child: Text(
                              value,
                              style: const TextStyle(fontFamily: 'Poppins'),
                            ),
                          ),
                        )
                        .toList(),
                    onChanged: (value) => setState(() => _origin = value),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppColors.primaryButton.withValues(alpha: 0.12),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Cadastro Rápido',
                    style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.w700,
                      color: AppColors.primaryButton,
                      fontFamily: 'Poppins',
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Preencha apenas os campos Brinco, Sexo e Lote para um cadastro rápido.',
                    style: TextStyle(
                      fontSize: 13,
                      color: AppColors.textSecondary,
                      fontFamily: 'Poppins',
                    ),
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    width: double.infinity,
                    child: OutlinedButton.icon(
                      onPressed: () =>
                          setState(() => _quickRegister = !_quickRegister),
                      icon: Icon(
                        _quickRegister ? Icons.check_circle : Icons.flash_on,
                        color: AppColors.primaryButton,
                      ),
                      label: Text(
                        _quickRegister
                            ? 'Cadastro rápido ativado'
                            : 'Usar cadastro rápido',
                        style: const TextStyle(
                          color: AppColors.primaryButton,
                          fontFamily: 'Poppins',
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      style: OutlinedButton.styleFrom(
                        minimumSize: const Size.fromHeight(60),
                        side: const BorderSide(color: AppColors.primaryButton),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                        padding: const EdgeInsets.symmetric(vertical: 16),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _step2() {
    return SingleChildScrollView(
      child: _card(
        title: 'Localização e Manejo',
        icon: Icons.location_on_outlined,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Fazenda',
              style: TextStyle(fontWeight: FontWeight.w500),
            ),
            const SizedBox(height: 8),
            InputDecorator(
              decoration: InputDecoration(
                filled: true,
                fillColor: AppColors.buttonDisabled.withValues(alpha: 0.12),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: Text(
                widget.propertyName,
                style: const TextStyle(fontFamily: 'Poppins'),
              ),
            ),
            const SizedBox(height: 16),
            _batchDropdown(),
            const SizedBox(height: 16),
            _dropdown(
              label: 'Pasto / Piquete',
              value: _pasture,
              items: ['Piquete 01', 'Piquete 02', 'Piquete 03'],
              onChanged: (v) => setState(() => _pasture = v),
            ),
            const SizedBox(height: 16),
            _dropdown(
              label: 'Sistema de Produção',
              value: _productionSystem,
              items: _productionSystems,
              onChanged: (v) => setState(() => _productionSystem = v),
            ),
            const SizedBox(height: 16),
            _dropdown(
              label: 'Status do animal',
              value: _animalStatus,
              items: _animalStatusOptions,
              onChanged: (v) => setState(() => _animalStatus = v),
            ),
            const SizedBox(height: 16),
            _dateField(
              label: 'Data de entrada no lote',
              value: _entryDate,
              onPick: (d) => setState(() => _entryDate = d),
            ),
            const SizedBox(height: 16),
            LabeledTextField(
              label: 'Observações',
              hintText: 'Opcional',
              controller: _notesController,
            ),
          ],
        ),
      ),
    );
  }

  Widget _step3() {
    return SingleChildScrollView(
      child: _card(
        title: 'Pesagem e desenvolvimento',
        icon: Icons.monitor_weight_outlined,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            LabeledTextField(
              label: 'Peso ao nascer (kg)',
              hintText: 'Ex: 32',
              controller: _birthWeightController,
              keyboardType: const TextInputType.numberWithOptions(
                decimal: true,
              ),
            ),
            const SizedBox(height: 16),
            _dateField(
              label: 'Data da pesagem',
              value: _birthDate,
              onPick: (d) => setState(() => _birthDate = d),
            ),
            const SizedBox(height: 16),
            _timeField(
              label: 'Hora',
              value: _birthDate,
              onTimePicked: (t) {
                if (_birthDate != null) {
                  setState(
                    () => _birthDate = DateTime(
                      _birthDate!.year,
                      _birthDate!.month,
                      _birthDate!.day,
                      t.hour,
                      t.minute,
                    ),
                  );
                }
              },
            ),
            const SizedBox(height: 16),
            LabeledTextField(
              label: 'Peso atual (kg)',
              hintText: 'Ex: 285.0',
              controller: _currentWeightController,
              keyboardType: const TextInputType.numberWithOptions(
                decimal: true,
              ),
            ),
            const SizedBox(height: 16),
            _dropdown(
              label: 'Condição corporal',
              value: _condition,
              items: _conditionOptions,
              onChanged: (v) => setState(() => _condition = v),
            ),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppColors.progressActive.withValues(alpha: 0.15),
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Row(
                children: [
                  Icon(
                    Icons.lightbulb_outline,
                    color: AppColors.primaryButton,
                    size: 18,
                  ),
                  SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      'Pesagens adicionais podem ser registradas após o cadastro.',
                      style: TextStyle(fontSize: 12, fontFamily: 'Poppins'),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _step4() {
    return SingleChildScrollView(
      child: _card(
        title: 'Genealogia',
        icon: Icons.biotech_outlined,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SwitchListTile(
              contentPadding: EdgeInsets.zero,
              title: const Text(
                'Este animal possui informações de genealogia?',
                style: TextStyle(fontSize: 14, fontFamily: 'Poppins'),
              ),
              value: _hasGenealogy,
              activeThumbColor: AppColors.primaryButton,
              onChanged: (v) => setState(() => _hasGenealogy = v),
            ),
            if (_hasGenealogy) ...[
              LabeledTextField(
                label: 'Nº registro / pedigree',
                hintText: 'Opcional',
                controller: _pedigreeController,
                keyboardType: TextInputType.number,
              ),
              const SizedBox(height: 16),
              const Text(
                'Pais',
                style: TextStyle(
                  fontWeight: FontWeight.w600,
                  fontFamily: 'Poppins',
                ),
              ),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(
                    child: LabeledTextField(
                      label: 'Pai',
                      hintText: 'Buscar pai',
                      controller: _fatherController,
                      suffixIcon: const Icon(Icons.search),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: LabeledTextField(
                      label: 'Mãe',
                      hintText: 'Buscar mãe',
                      controller: _motherController,
                      suffixIcon: const Icon(Icons.search),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              const Text(
                'Avós paternos (opcional)',
                style: TextStyle(
                  fontWeight: FontWeight.w600,
                  fontFamily: 'Poppins',
                ),
              ),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(
                    child: LabeledTextField(
                      label: 'Avô paterno',
                      hintText: 'Buscar avô paterno',
                      controller: _paternalGrandfatherController,
                      suffixIcon: const Icon(Icons.search),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: LabeledTextField(
                      label: 'Avó paterna',
                      hintText: 'Buscar avó paterna',
                      controller: _paternalGrandmotherController,
                      suffixIcon: const Icon(Icons.search),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              const Text(
                'Avós maternos (opcional)',
                style: TextStyle(
                  fontWeight: FontWeight.w600,
                  fontFamily: 'Poppins',
                ),
              ),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(
                    child: LabeledTextField(
                      label: 'Avô materno',
                      hintText: 'Buscar avô materno',
                      controller: _maternalGrandfatherController,
                      suffixIcon: const Icon(Icons.search),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: LabeledTextField(
                      label: 'Avó materna',
                      hintText: 'Buscar avó materna',
                      controller: _maternalGrandmotherController,
                      suffixIcon: const Icon(Icons.search),
                    ),
                  ),
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _step5() {
    return SingleChildScrollView(
      child: _card(
        title: 'Resumo',
        icon: Icons.check_circle_outline,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _summaryRow('Brinco', _brincoController.text),
            _summaryRow(
              'Nome',
              _nameController.text.isEmpty ? '—' : _nameController.text,
            ),
            _summaryRow('Sexo', _sex == 'F' ? 'Fêmea' : 'Macho'),
            _summaryRow('Categoria', _category ?? '—'),
            _summaryRow(
              'Raça',
              _breedController.text.isEmpty ? '—' : _breedController.text,
            ),
            _summaryRow(
              'Nascimento',
              _birthDate != null ? _isoDate(_birthDate!) : '—',
            ),
            _summaryRow('Origem', _origin ?? '—'),
            if (_batchId != null) _summaryRow('Lote', '#$_batchId'),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppColors.progressActive.withValues(alpha: 0.15),
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Text(
                'Ao confirmar, o animal será cadastrado e estará disponível no inventário.',
                style: TextStyle(fontSize: 12, fontFamily: 'Poppins'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _summaryRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 110,
            child: Text(
              label,
              style: const TextStyle(
                color: AppColors.textSecondary,
                fontSize: 13,
                fontFamily: 'Poppins',
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

  Widget _timeField({
    required String label,
    required DateTime? value,
    required ValueChanged<TimeOfDay> onTimePicked,
  }) {
    final textValue = value != null
        ? '${value.hour.toString().padLeft(2, '0')}:${value.minute.toString().padLeft(2, '0')}'
        : null;
    return GestureDetector(
      onTap: () async {
        final current = value != null
            ? TimeOfDay.fromDateTime(value)
            : TimeOfDay.now();
        final picked = await showTimePicker(
          context: context,
          initialTime: current,
        );
        if (picked != null) onTimePicked(picked);
      },
      child: InputDecorator(
        decoration: InputDecoration(
          labelText: label,
          filled: true,
          fillColor: Colors.white,
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              textValue ?? 'Selecione a hora',
              style: TextStyle(
                color: textValue != null ? Colors.black : Colors.grey.shade500,
                fontFamily: 'Poppins',
              ),
            ),
            const Icon(Icons.access_time, color: AppColors.primaryButton),
          ],
        ),
      ),
    );
  }

  Widget _batchDropdown() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Lote/Grupo',
          style: TextStyle(fontWeight: FontWeight.w500, fontFamily: 'Poppins'),
        ),
        const SizedBox(height: 8),
        DropdownButtonFormField<int>(
          initialValue: _batchId,
          decoration: InputDecoration(
            filled: true,
            fillColor: Colors.white,
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          ),
          hint: const Text('Selecione (opcional)'),
          items: _batches.map((b) {
            final batchId = b['id_batch'] ?? b['id'];
            final value = batchId is int
                ? batchId
                : int.tryParse(batchId?.toString() ?? '');
            return DropdownMenuItem<int>(
              value: value,
              child: Text(b['name']?.toString() ?? 'Lote'),
            );
          }).toList(),
          onChanged: (v) => setState(() => _batchId = v),
        ),
      ],
    );
  }

  Widget _dropdown({
    required String label,
    required String? value,
    required List<String> items,
    required ValueChanged<String?> onChanged,
    Map<String, String>? display,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: const TextStyle(fontWeight: FontWeight.w500)),
        const SizedBox(height: 8),
        DropdownButtonFormField<String>(
          initialValue: value,
          decoration: InputDecoration(
            filled: true,
            fillColor: Colors.white,
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          ),
          hint: const Text('Selecione'),
          items: items
              .map(
                (e) =>
                    DropdownMenuItem(value: e, child: Text(display?[e] ?? e)),
              )
              .toList(),
          onChanged: onChanged,
        ),
      ],
    );
  }

  Widget _dateField({
    required String label,
    required DateTime? value,
    required ValueChanged<DateTime> onPick,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: const TextStyle(fontWeight: FontWeight.w500)),
        const SizedBox(height: 8),
        InkWell(
          onTap: () => _pickDate(onPicked: onPick, initial: value),
          borderRadius: BorderRadius.circular(12),
          child: InputDecorator(
            decoration: InputDecoration(
              filled: true,
              fillColor: Colors.white,
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              suffixIcon: const Icon(Icons.calendar_today, size: 18),
            ),
            child: Text(
              value != null
                  ? '${value.day.toString().padLeft(2, '0')}/${value.month.toString().padLeft(2, '0')}/${value.year}'
                  : 'Selecione a data',
              style: TextStyle(
                color: value != null ? Colors.black : AppColors.hintText,
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _footer() {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          Expanded(
            child: SizedBox(
              height: 60,
              child: OutlinedButton(
                onPressed: _submitting ? null : _back,
                style: OutlinedButton.styleFrom(
                  minimumSize: const Size.fromHeight(60),
                  side: const BorderSide(color: AppColors.primaryButton),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text(
                  'Voltar',
                  style: TextStyle(fontFamily: 'Poppins'),
                ),
              ),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            flex: 2,
            child: SizedBox(
              height: 60,
              child: PrimaryButton(
                text: _submitting
                    ? 'Salvando...'
                    : (_step == 5 ? 'Confirmar e salvar' : 'Continuar'),
                onPressed: _submitting ? null : _next,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _SexToggle extends StatelessWidget {
  const _SexToggle({
    required this.label,
    required this.icon,
    required this.selected,
    required this.onTap,
  });

  final String label;
  final IconData icon;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 14),
        decoration: BoxDecoration(
          color: selected
              ? AppColors.progressActive.withValues(alpha: 0.2)
              : Colors.white,
          border: Border.all(
            color: selected ? AppColors.primaryButton : Colors.grey.shade300,
            width: selected ? 2 : 1,
          ),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Column(
          children: [
            Icon(icon, color: AppColors.primaryButton),
            const SizedBox(height: 4),
            Text(label, style: const TextStyle(fontFamily: 'Poppins')),
          ],
        ),
      ),
    );
  }
}


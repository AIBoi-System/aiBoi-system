import 'package:ai_boi/core/widgets/labeled_text_field.dart';
import 'package:flutter/material.dart';

import 'animal_form_data.dart';

class AnimalRegisterStep1Identification extends StatefulWidget {
  const AnimalRegisterStep1Identification({
    super.key,
    required this.formData,
    required this.formKey,
  });

  final AnimalFormData formData;
  final GlobalKey<FormState> formKey;

  @override
  State<AnimalRegisterStep1Identification> createState() =>
      _AnimalRegisterStep1IdentificationState();
}

class _AnimalRegisterStep1IdentificationState
    extends State<AnimalRegisterStep1Identification> {
  late final TextEditingController _brincoController;
  late final TextEditingController _nameController;
  late final TextEditingController _racaController;

  @override
  void initState() {
    super.initState();
    _brincoController = TextEditingController(
      text: widget.formData.brinco?.toString() ?? '',
    );
    _nameController = TextEditingController(text: widget.formData.nome ?? '');
    _racaController = TextEditingController(text: widget.formData.raca ?? '');

    _brincoController.addListener(() {
      final val = int.tryParse(_brincoController.text);
      widget.formData.brinco = val;
    });
    _nameController.addListener(() {
      widget.formData.nome = _nameController.text;
    });
    _racaController.addListener(() {
      widget.formData.raca = _racaController.text;
    });
  }

  @override
  void dispose() {
    _brincoController.dispose();
    _nameController.dispose();
    _racaController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: widget.formKey,
      child: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Identificação do Animal',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                fontFamily: 'Poppins',
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              'Preencha os dados básicos para identificar o animal no sistema.',
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),
            const SizedBox(height: 24),
            LabeledTextField(
              label: 'Brinco (obrigatório)',
              hintText: 'Ex: 1234',
              controller: _brincoController,
              keyboardType: TextInputType.number,
              validator: (val) {
                if (val == null || val.trim().isEmpty) {
                  return 'Informe o brinco';
                }
                if (int.tryParse(val) == null) {
                  return 'Brinco deve ser numérico';
                }
                return null;
              },
            ),
            const SizedBox(height: 16),
            LabeledTextField(
              label: 'Nome / Apelido (opcional)',
              hintText: 'Ex: Estrela',
              controller: _nameController,
            ),
            const SizedBox(height: 16),
            LabeledTextField(
              label: 'Raça (opcional)',
              hintText: 'Ex: Nelore',
              controller: _racaController,
            ),
          ],
        ),
      ),
    );
  }
}

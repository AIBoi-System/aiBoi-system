import 'package:flutter/material.dart';
import 'animal_form_data.dart';

class AnimalRegisterStep5Genealogy extends StatefulWidget {
  const AnimalRegisterStep5Genealogy({
    super.key,
    required this.formData,
    required this.formKey,
  });

  final AnimalFormData formData;
  final GlobalKey<FormState> formKey;

  @override
  State<AnimalRegisterStep5Genealogy> createState() =>
      _AnimalRegisterStep5GenealogyState();
}

class _AnimalRegisterStep5GenealogyState
    extends State<AnimalRegisterStep5Genealogy> {
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
              'Genealogia (Opcional)',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                fontFamily: 'Poppins',
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              'Informe a filiação e o grau de sangue.',
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),
            const SizedBox(height: 24),
            TextFormField(
              initialValue: widget.formData.pai ?? '',
              decoration: const InputDecoration(
                labelText: 'Pai (Brinco ou Nome)',
                border: OutlineInputBorder(),
              ),
              onChanged: (val) => widget.formData.pai = val,
            ),
            const SizedBox(height: 16),
            TextFormField(
              initialValue: widget.formData.mae ?? '',
              decoration: const InputDecoration(
                labelText: 'Mãe (Brinco ou Nome)',
                border: OutlineInputBorder(),
              ),
              onChanged: (val) => widget.formData.mae = val,
            ),
            const SizedBox(height: 16),
            TextFormField(
              initialValue: widget.formData.avoPaterno ?? '',
              decoration: const InputDecoration(
                labelText: 'Avô Paterno',
                border: OutlineInputBorder(),
              ),
              onChanged: (val) => widget.formData.avoPaterno = val,
            ),
            const SizedBox(height: 16),
            TextFormField(
              initialValue: widget.formData.avoMaterno ?? '',
              decoration: const InputDecoration(
                labelText: 'Avô Materno',
                border: OutlineInputBorder(),
              ),
              onChanged: (val) => widget.formData.avoMaterno = val,
            ),
            const SizedBox(height: 16),
            TextFormField(
              initialValue: widget.formData.pedigreePo?.toString() ?? '',
              decoration: const InputDecoration(
                labelText: 'Registro Pedigree PO',
                border: OutlineInputBorder(),
              ),
              keyboardType: TextInputType.number,
              onChanged: (val) => widget.formData.pedigreePo = int.tryParse(val),
            ),
          ],
        ),
      ),
    );
  }
}

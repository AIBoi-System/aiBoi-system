import 'package:flutter/material.dart';
import 'animal_form_data.dart';

class AnimalRegisterStep6Development extends StatefulWidget {
  const AnimalRegisterStep6Development({
    super.key,
    required this.formData,
    required this.formKey,
  });

  final AnimalFormData formData;
  final GlobalKey<FormState> formKey;

  @override
  State<AnimalRegisterStep6Development> createState() =>
      _AnimalRegisterStep6DevelopmentState();
}

class _AnimalRegisterStep6DevelopmentState
    extends State<AnimalRegisterStep6Development> {
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
              'Desenvolvimento (Pesos)',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                fontFamily: 'Poppins',
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              'Informe os dados de peso para acompanhamento.',
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),
            const SizedBox(height: 24),
            TextFormField(
              initialValue: widget.formData.pesoNascer?.toString() ?? '',
              decoration: const InputDecoration(
                labelText: 'Peso ao Nascer (kg)',
                border: OutlineInputBorder(),
              ),
              keyboardType: TextInputType.numberWithOptions(decimal: true),
              onChanged: (val) {
                widget.formData.pesoNascer = double.tryParse(val.replaceAll(',', '.'));
              },
            ),
            const SizedBox(height: 16),
            TextFormField(
              initialValue: widget.formData.pesoAtual?.toString() ?? '',
              decoration: const InputDecoration(
                labelText: 'Peso Atual (kg)',
                border: OutlineInputBorder(),
              ),
              keyboardType: TextInputType.numberWithOptions(decimal: true),
              onChanged: (val) {
                widget.formData.pesoAtual = double.tryParse(val.replaceAll(',', '.'));
              },
            ),
          ],
        ),
      ),
    );
  }
}

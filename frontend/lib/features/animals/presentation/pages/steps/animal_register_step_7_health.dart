import 'package:flutter/material.dart';
import 'animal_form_data.dart';

class AnimalRegisterStep7Health extends StatefulWidget {
  const AnimalRegisterStep7Health({
    super.key,
    required this.formData,
    required this.formKey,
  });

  final AnimalFormData formData;
  final GlobalKey<FormState> formKey;

  @override
  State<AnimalRegisterStep7Health> createState() =>
      _AnimalRegisterStep7HealthState();
}

class _AnimalRegisterStep7HealthState extends State<AnimalRegisterStep7Health> {
  static const _animalStatusOptions = ['Ativo', 'Inativo', 'Morto'];
  static const _conditionOptions = ['Magro', 'Ideal', 'Gordo'];

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
              'Saúde e Manejo',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                fontFamily: 'Poppins',
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              'Informe o status do animal e anotações extras.',
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),
            const SizedBox(height: 24),
            DropdownButtonFormField<String>(
              value: widget.formData.statusAnimal == 'ATIVO' ? 'Ativo' : widget.formData.statusAnimal,
              decoration: const InputDecoration(
                labelText: 'Status do Animal',
                border: OutlineInputBorder(),
              ),
              items: _animalStatusOptions.map((s) {
                return DropdownMenuItem(value: s, child: Text(s));
              }).toList(),
              onChanged: (val) {
                setState(() {
                  widget.formData.statusAnimal = val?.toUpperCase() ?? 'ATIVO';
                });
              },
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: widget.formData.condicaoCorporal,
              decoration: const InputDecoration(
                labelText: 'Condição Corporal (opcional)',
                border: OutlineInputBorder(),
              ),
              items: _conditionOptions.map((s) {
                return DropdownMenuItem(value: s, child: Text(s));
              }).toList(),
              onChanged: (val) {
                setState(() {
                  widget.formData.condicaoCorporal = val;
                });
              },
            ),
            const SizedBox(height: 16),
            TextFormField(
              initialValue: widget.formData.notas ?? '',
              decoration: const InputDecoration(
                labelText: 'Observações e Anotações',
                border: OutlineInputBorder(),
              ),
              maxLines: 3,
              onChanged: (val) => widget.formData.notas = val,
            ),
          ],
        ),
      ),
    );
  }
}

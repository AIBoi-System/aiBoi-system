import 'package:flutter/material.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'animal_form_data.dart';

class AnimalRegisterStep2Category extends StatefulWidget {
  const AnimalRegisterStep2Category({
    super.key,
    required this.formData,
    required this.formKey,
  });

  final AnimalFormData formData;
  final GlobalKey<FormState> formKey;

  @override
  State<AnimalRegisterStep2Category> createState() =>
      _AnimalRegisterStep2CategoryState();
}

class _AnimalRegisterStep2CategoryState
    extends State<AnimalRegisterStep2Category> {
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
              'Categoria e Sexo',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                fontFamily: 'Poppins',
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              'Informe o sexo e a categoria atual do animal.',
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),
            const SizedBox(height: 24),
            const Text('Sexo', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(
                  child: _buildRadioTile(
                    title: 'Fêmea',
                    value: 'F',
                    groupValue: widget.formData.sexo,
                    onChanged: (val) {
                      setState(() {
                        widget.formData.sexo = val!;
                        if (val == 'M') {
                          widget.formData.statusReprodutivo = null;
                        }
                      });
                    },
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: _buildRadioTile(
                    title: 'Macho',
                    value: 'M',
                    groupValue: widget.formData.sexo,
                    onChanged: (val) {
                      setState(() {
                        widget.formData.sexo = val!;
                        widget.formData.statusReprodutivo = null;
                      });
                    },
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),
            DropdownButtonFormField<String>(
              value: widget.formData.categoria,
              decoration: const InputDecoration(
                labelText: 'Categoria (obrigatório)',
                border: OutlineInputBorder(),
              ),
              items: _categories.map((c) {
                return DropdownMenuItem(value: c, child: Text(c));
              }).toList(),
              onChanged: (val) {
                setState(() {
                  widget.formData.categoria = val;
                });
              },
              validator: (val) => val == null ? 'Selecione a categoria' : null,
            ),
            if (widget.formData.sexo == 'F') ...[
              const SizedBox(height: 24),
              DropdownButtonFormField<String>(
                value: widget.formData.statusReprodutivo,
                decoration: const InputDecoration(
                  labelText: 'Status Reprodutivo (obrigatório)',
                  border: OutlineInputBorder(),
                ),
                items: _reproductiveStatuses.map((s) {
                  return DropdownMenuItem(value: s, child: Text(s));
                }).toList(),
                onChanged: (val) {
                  setState(() {
                    widget.formData.statusReprodutivo = val;
                  });
                },
                validator: (val) =>
                    val == null ? 'Selecione o status reprodutivo' : null,
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildRadioTile({
    required String title,
    required String value,
    required String groupValue,
    required ValueChanged<String?> onChanged,
  }) {
    final selected = value == groupValue;
    return GestureDetector(
      onTap: () => onChanged(value),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 8),
        decoration: BoxDecoration(
          color: selected ? AppColors.primaryButton.withOpacity(0.1) : Colors.white,
          border: Border.all(
            color: selected ? AppColors.primaryButton : Colors.grey.shade300,
            width: selected ? 2 : 1,
          ),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Row(
          children: [
            Radio<String>(
              value: value,
              groupValue: groupValue,
              onChanged: onChanged,
              activeColor: AppColors.primaryButton,
              materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
            ),
            Expanded(
              child: Text(
                title,
                style: TextStyle(
                  fontWeight: selected ? FontWeight.bold : FontWeight.normal,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

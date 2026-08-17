import 'package:flutter/material.dart';
import 'animal_form_data.dart';
import 'package:intl/intl.dart';

class AnimalRegisterStep3Dates extends StatefulWidget {
  const AnimalRegisterStep3Dates({
    super.key,
    required this.formData,
    required this.formKey,
  });

  final AnimalFormData formData;
  final GlobalKey<FormState> formKey;

  @override
  State<AnimalRegisterStep3Dates> createState() =>
      _AnimalRegisterStep3DatesState();
}

class _AnimalRegisterStep3DatesState extends State<AnimalRegisterStep3Dates> {
  static const _origins = ['PROPRIEDADE', 'COMPRA', 'TRANSFERENCIA'];
  final _dateFormat = DateFormat('dd/MM/yyyy');

  Future<void> _pickDate(
      BuildContext context, DateTime? initial, ValueChanged<DateTime> onPicked) async {
    final picked = await showDatePicker(
      context: context,
      initialDate: initial ?? DateTime.now(),
      firstDate: DateTime(1990),
      lastDate: DateTime.now(),
    );
    if (picked != null) {
      onPicked(picked);
    }
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
              'Datas e Origem',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                fontFamily: 'Poppins',
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              'Informe quando o animal nasceu e como entrou no sistema.',
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),
            const SizedBox(height: 24),
            _buildDateField(
              label: 'Data de Nascimento (obrigatório)',
              value: widget.formData.dataNascimento,
              onTap: () => _pickDate(context, widget.formData.dataNascimento, (d) {
                setState(() => widget.formData.dataNascimento = d);
              }),
              validator: (v) => widget.formData.dataNascimento == null
                  ? 'Informe a data de nascimento'
                  : null,
            ),
            const SizedBox(height: 16),
            _buildDateField(
              label: 'Data de Entrada (opcional)',
              value: widget.formData.dataEntrada,
              onTap: () => _pickDate(context, widget.formData.dataEntrada, (d) {
                setState(() => widget.formData.dataEntrada = d);
              }),
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: widget.formData.origem,
              decoration: const InputDecoration(
                labelText: 'Origem (obrigatório)',
                border: OutlineInputBorder(),
              ),
              items: _origins.map((o) {
                return DropdownMenuItem(value: o, child: Text(o));
              }).toList(),
              onChanged: (val) {
                setState(() {
                  widget.formData.origem = val;
                });
              },
              validator: (val) => val == null ? 'Selecione a origem' : null,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDateField({
    required String label,
    required DateTime? value,
    required VoidCallback onTap,
    String? Function(String?)? validator,
  }) {
    return TextFormField(
      readOnly: true,
      onTap: onTap,
      decoration: InputDecoration(
        labelText: label,
        border: const OutlineInputBorder(),
        suffixIcon: const Icon(Icons.calendar_today),
      ),
      controller: TextEditingController(
        text: value != null ? _dateFormat.format(value) : '',
      ),
      validator: validator,
    );
  }
}

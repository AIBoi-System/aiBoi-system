import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'animal_form_data.dart';

class AnimalRegisterStep8Summary extends StatelessWidget {
  const AnimalRegisterStep8Summary({
    super.key,
    required this.formData,
  });

  final AnimalFormData formData;

  @override
  Widget build(BuildContext context) {
    final dateFormat = DateFormat('dd/MM/yyyy');
    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Resumo do Cadastro',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              fontFamily: 'Poppins',
            ),
          ),
          const SizedBox(height: 8),
          const Text(
            'Verifique se todas as informações estão corretas antes de finalizar.',
            style: TextStyle(fontSize: 14, color: Colors.grey),
          ),
          const SizedBox(height: 24),
          _buildSummarySection('Identificação', [
            'Brinco: ${formData.brinco ?? "-"}',
            'Nome: ${formData.nome?.isEmpty ?? true ? "-" : formData.nome}',
            'Raça: ${formData.raca?.isEmpty ?? true ? "-" : formData.raca}',
          ]),
          _buildSummarySection('Categoria e Sexo', [
            'Sexo: ${formData.sexo == "F" ? "Fêmea" : "Macho"}',
            'Categoria: ${formData.categoria ?? "-"}',
            if (formData.sexo == "F") 'Status Reprodutivo: ${formData.statusReprodutivo ?? "-"}',
          ]),
          _buildSummarySection('Datas e Origem', [
            'Nascimento: ${formData.dataNascimento != null ? dateFormat.format(formData.dataNascimento!) : "-"}',
            'Entrada: ${formData.dataEntrada != null ? dateFormat.format(formData.dataEntrada!) : "-"}',
            'Origem: ${formData.origem ?? "-"}',
          ]),
          _buildSummarySection('Localização', [
            'Lote: ${formData.loteId ?? "-"}',
          ]),
          const SizedBox(height: 32),
        ],
      ),
    );
  }

  Widget _buildSummarySection(String title, List<String> items) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          const SizedBox(height: 8),
          ...items.map((item) => Padding(
                padding: const EdgeInsets.only(bottom: 4),
                child: Text(item, style: const TextStyle(fontSize: 14)),
              )),
          const Divider(),
        ],
      ),
    );
  }
}

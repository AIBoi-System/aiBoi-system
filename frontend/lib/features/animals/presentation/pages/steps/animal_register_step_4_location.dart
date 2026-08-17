import 'package:flutter/material.dart';
import 'animal_form_data.dart';
import 'package:ai_boi/features/animals/data/datasources/animal_remote_data_source.dart';

class AnimalRegisterStep4Location extends StatefulWidget {
  const AnimalRegisterStep4Location({
    super.key,
    required this.formData,
    required this.formKey,
    required this.dataSource,
  });

  final AnimalFormData formData;
  final GlobalKey<FormState> formKey;
  final AnimalRemoteDataSource dataSource;

  @override
  State<AnimalRegisterStep4Location> createState() =>
      _AnimalRegisterStep4LocationState();
}

class _AnimalRegisterStep4LocationState
    extends State<AnimalRegisterStep4Location> {
  static const _productionSystems = ['Cria', 'Recria', 'Engorda', 'Leite'];
  List<Map<String, dynamic>> _batches = [];
  bool _isLoadingBatches = true;

  @override
  void initState() {
    super.initState();
    _loadBatches();
  }

  Future<void> _loadBatches() async {
    try {
      final batches = await widget.dataSource.listBatches();
      if (mounted) {
        setState(() {
          _batches = batches.cast<Map<String, dynamic>>();
          _isLoadingBatches = false;
        });
      }
    } catch (_) {
      if (mounted) {
        setState(() => _isLoadingBatches = false);
      }
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
              'Localização e Sistema',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                fontFamily: 'Poppins',
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              'A qual lote e pasto este animal pertence?',
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),
            const SizedBox(height: 24),
            _isLoadingBatches
                ? const Center(child: CircularProgressIndicator())
                : DropdownButtonFormField<int>(
                    value: widget.formData.loteId,
                    decoration: const InputDecoration(
                      labelText: 'Lote (obrigatório)',
                      border: OutlineInputBorder(),
                    ),
                    items: _batches.map((b) {
                      return DropdownMenuItem<int>(
                        value: b['id_batch'] as int,
                        child: Text(b['batch_name'].toString()),
                      );
                    }).toList(),
                    onChanged: (val) {
                      setState(() {
                        widget.formData.loteId = val;
                      });
                    },
                    validator: (val) => val == null ? 'Selecione o lote' : null,
                  ),
            const SizedBox(height: 16),
            TextFormField(
              initialValue: widget.formData.pasto ?? '',
              decoration: const InputDecoration(
                labelText: 'Pasto (opcional)',
                border: OutlineInputBorder(),
              ),
              onChanged: (val) => widget.formData.pasto = val,
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: widget.formData.sistemaProducao,
              decoration: const InputDecoration(
                labelText: 'Sistema de Produção (opcional)',
                border: OutlineInputBorder(),
              ),
              items: _productionSystems.map((s) {
                return DropdownMenuItem(value: s, child: Text(s));
              }).toList(),
              onChanged: (val) {
                setState(() {
                  widget.formData.sistemaProducao = val;
                });
              },
            ),
          ],
        ),
      ),
    );
  }
}

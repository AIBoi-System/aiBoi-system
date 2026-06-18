import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/labeled_text_field.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_cubit.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_state.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class PropertyFormPage extends StatefulWidget {
  const PropertyFormPage({super.key});

  @override
  State<PropertyFormPage> createState() => _PropertyFormPageState();
}

class _PropertyFormPageState extends State<PropertyFormPage> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  String? _selectedType;
  final _areaController = TextEditingController();
  final _cityController = TextEditingController();

  static const _types = ['Cria', 'Corte', 'Leite', 'Mista', 'Recria'];

  @override
  void dispose() {
    _nameController.dispose();
    _areaController.dispose();
    _cityController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<RegistrationCubit, RegistrationState>(
      listener: (context, state) {
        if (state is RegistrationPropertyCreated) {
          Navigator.pushReplacementNamed(
            context,
            AppRouter.propertySuccess,
            arguments: state.property,
          );
        } else if (state is RegistrationError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message), backgroundColor: Colors.red),
          );
        }
      },
      builder: (context, state) {
        final isLoading = state is RegistrationLoading;
        return Scaffold(
          backgroundColor: AppColors.backgroundScreen,
          appBar: AppBar(
            backgroundColor: AppColors.backgroundScreen,
            elevation: 0,
            leading: IconButton(
              icon: const Icon(Icons.arrow_back, color: Colors.black),
              onPressed: () => Navigator.pop(context),
            ),
            title: const Text(
              'Cadastrar propriedade',
              style: TextStyle(
                color: Colors.black,
                fontSize: 16,
                fontWeight: FontWeight.w600,
                fontFamily: 'Poppins',
              ),
            ),
            centerTitle: true,
          ),
          body: SafeArea(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Adicione uma nova fazenda ao sistema para começar a gerenciar seus dados.',
                      style: TextStyle(
                        color: AppColors.textSecondary,
                        fontSize: 14,
                        fontFamily: 'Poppins',
                      ),
                    ),
                    const SizedBox(height: 20),
                    _SectionCard(
                      icon: Icons.home_work_outlined,
                      title: 'Dados da propriedade',
                      subtitle: 'Informe os principais dados da sua propriedade',
                      children: [
                        LabeledTextField(
                          label: 'Nome da propriedade',
                          hintText: 'Ex: Sabiá dourado',
                          controller: _nameController,
                          validator: (v) =>
                              v == null || v.isEmpty ? 'Informe o nome' : null,
                        ),
                        const SizedBox(height: 16),
                        DropdownButtonFormField<String>(
                          initialValue: _selectedType,
                          decoration: InputDecoration(
                            labelText: 'Tipo da propriedade',
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                          items: _types
                              .map((t) => DropdownMenuItem(value: t, child: Text(t)))
                              .toList(),
                          onChanged: (v) => setState(() => _selectedType = v),
                          validator: (v) =>
                              v == null || v.isEmpty ? 'Selecione o tipo' : null,
                        ),
                        const SizedBox(height: 16),
                        LabeledTextField(
                          label: 'Área (Hectare)',
                          hintText: 'Ex: 500',
                          controller: _areaController,
                          keyboardType: TextInputType.number,
                          validator: (v) {
                            if (v == null || v.isEmpty) return 'Informe a área';
                            if (double.tryParse(v.replaceAll(',', '.')) == null) {
                              return 'Área inválida';
                            }
                            return null;
                          },
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    _SectionCard(
                      icon: Icons.location_on_outlined,
                      title: 'Localização',
                      subtitle: 'Informações de localização da propriedade',
                      children: [
                        LabeledTextField(
                          label: 'Cidade/Estado',
                          hintText: 'Ex: Anapú - PA',
                          controller: _cityController,
                          validator: (v) =>
                              v == null || v.isEmpty ? 'Informe cidade/estado' : null,
                        ),
                      ],
                    ),
                    const SizedBox(height: 24),
                    PrimaryButton(
                      text: isLoading ? 'Salvando...' : 'Salvar Propriedade',
                      onPressed: isLoading ? null : _submit,
                    ),
                    const SizedBox(height: 12),
                    SizedBox(
                      width: double.infinity,
                      height: 50,
                      child: OutlinedButton(
                        onPressed: () {
                          Navigator.pushNamedAndRemoveUntil(
                            context,
                            AppRouter.home,
                            (route) => false,
                          );
                        },
                        style: OutlinedButton.styleFrom(
                          side: const BorderSide(color: AppColors.primaryGreen),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                        ),
                        child: const Text(
                          'Cancelar',
                          style: TextStyle(
                            color: AppColors.primaryGreen,
                            fontWeight: FontWeight.bold,
                            fontFamily: 'Poppins',
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        );
      },
    );
  }

  void _submit() {
    if (!_formKey.currentState!.validate()) return;
    if (_selectedType == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Selecione o tipo da propriedade')),
      );
      return;
    }
    context.read<RegistrationCubit>().createProperty(
          PropertyDraft(
            name: _nameController.text.trim(),
            propertyType: _selectedType!,
            sizeHectares:
                double.parse(_areaController.text.trim().replaceAll(',', '.')),
            cityState: _cityController.text.trim(),
          ),
        );
  }
}

class _SectionCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final List<Widget> children;

  const _SectionCard({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.children,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 12,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: AppColors.sectionGreen, size: 22),
              const SizedBox(width: 8),
              Text(
                title,
                style: const TextStyle(
                  color: AppColors.sectionGreen,
                  fontWeight: FontWeight.w600,
                  fontFamily: 'Poppins',
                ),
              ),
            ],
          ),
          const SizedBox(height: 4),
          Text(
            subtitle,
            style: const TextStyle(
              color: AppColors.textSecondary,
              fontSize: 12,
              fontFamily: 'Poppins',
            ),
          ),
          const SizedBox(height: 16),
          ...children,
        ],
      ),
    );
  }
}


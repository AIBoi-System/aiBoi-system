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
  final _areaController = TextEditingController();
  final _cityController = TextEditingController();
  String? _selectedType;
  static const _types = ['Cria', 'Corte', 'Leite', 'Mista', 'Recria'];

  @override
  void dispose() {
    _nameController.dispose();
    _areaController.dispose();
    _cityController.dispose();
    super.dispose();
  }

  @override
  Widget build(
    BuildContext context,
  ) => BlocConsumer<RegistrationCubit, RegistrationState>(
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
      final loading = state is RegistrationLoading;
      return Scaffold(
        backgroundColor: AppColors.figmaBackground,
        appBar: AppBar(
          backgroundColor: AppColors.figmaBackground,
          surfaceTintColor: AppColors.figmaBackground,
          leading: IconButton(
            onPressed: () => Navigator.maybePop(context),
            icon: const Icon(Icons.arrow_back, color: AppColors.figmaText),
          ),
          title: const Text(
            'Cadastrar propriedade',
            style: TextStyle(
              color: AppColors.figmaText,
              fontSize: 16,
              fontWeight: FontWeight.w700,
              fontFamily: 'Poppins',
            ),
          ),
          centerTitle: true,
        ),
        body: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.fromLTRB(20, 4, 20, 28),
            child: Form(
              key: _formKey,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Expanded(
                        child: Text(
                          'Adicione uma nova fazenda ao\nsistema para começar a gerenciar\nseus dados',
                          style: TextStyle(
                            color: AppColors.figmaMuted,
                            fontSize: 13,
                            height: 1.45,
                          ),
                        ),
                      ),
                      Image.asset(
                        'assets/images/figma_property_form_header.png',
                        width: 150,
                        height: 83,
                        fit: BoxFit.contain,
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Container(
                    padding: const EdgeInsets.fromLTRB(20, 22, 20, 20),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(16),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withValues(alpha: .05),
                          blurRadius: 15,
                          offset: const Offset(0, 8),
                        ),
                      ],
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const _FormSectionHeader(
                          icon: Icons.eco_rounded,
                          title: 'Dados da propriedade',
                          subtitle:
                              'Informe os principais dados da sua propriedade',
                        ),
                        const SizedBox(height: 18),
                        LabeledTextField(
                          label: 'Nome da propriedade',
                          hintText: 'Ex: Sabiá dourado',
                          controller: _nameController,
                          validator: (v) => v == null || v.trim().isEmpty
                              ? 'Informe o nome'
                              : null,
                        ),
                        const SizedBox(height: 14),
                        const Text(
                          'Tipo da propriedade',
                          style: TextStyle(
                            color: AppColors.figmaText,
                            fontSize: 13,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        const SizedBox(height: 7),
                        DropdownButtonFormField<String>(
                          initialValue: _selectedType,
                          hint: const Text(
                            'Ex: Cria',
                            style: TextStyle(
                              color: Color(0xFFA7B0AB),
                              fontSize: 13,
                            ),
                          ),
                          decoration: InputDecoration(
                            contentPadding: const EdgeInsets.symmetric(
                              horizontal: 15,
                              vertical: 15,
                            ),
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(12),
                              borderSide: const BorderSide(
                                color: AppColors.figmaBorder,
                              ),
                            ),
                            enabledBorder: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(12),
                              borderSide: const BorderSide(
                                color: AppColors.figmaBorder,
                              ),
                            ),
                          ),
                          items: _types
                              .map(
                                (type) => DropdownMenuItem(
                                  value: type,
                                  child: Text(type),
                                ),
                              )
                              .toList(),
                          onChanged: (value) =>
                              setState(() => _selectedType = value),
                          validator: (value) =>
                              value == null ? 'Selecione o tipo' : null,
                        ),
                        const SizedBox(height: 14),
                        LabeledTextField(
                          label: 'Área (Hectare)',
                          hintText: 'Ex: 500',
                          controller: _areaController,
                          keyboardType: TextInputType.number,
                          validator: (v) {
                            if (v == null || v.isEmpty) {
                              return 'Informe a área';
                            }
                            if (double.tryParse(v.replaceAll(',', '.')) ==
                                null) {
                              return 'Área inválida';
                            }
                            return null;
                          },
                        ),
                        const Padding(
                          padding: EdgeInsets.symmetric(vertical: 18),
                          child: Divider(height: 1),
                        ),
                        const _FormSectionHeader(
                          icon: Icons.location_on_rounded,
                          title: 'Localização',
                          subtitle: 'Informações de localização da propriedade',
                        ),
                        const SizedBox(height: 18),
                        LabeledTextField(
                          label: 'Cidade/Estado',
                          hintText: 'Ex: Anapú - PA',
                          controller: _cityController,
                          validator: (v) => v == null || v.trim().isEmpty
                              ? 'Informe cidade/estado'
                              : null,
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),
                  PrimaryButton(
                    text: loading ? 'Salvando...' : 'Salvar Propriedade',
                    onPressed: loading ? null : _submit,
                  ),
                  const SizedBox(height: 10),
                  SizedBox(
                    width: double.infinity,
                    height: 52,
                    child: OutlinedButton(
                      onPressed: () => Navigator.pushNamedAndRemoveUntil(
                        context,
                        AppRouter.properties,
                        (_) => false,
                      ),
                      style: OutlinedButton.styleFrom(
                        backgroundColor: Colors.white,
                        foregroundColor: AppColors.figmaPrimary,
                        side: BorderSide.none,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                      child: const Text(
                        'Cancelar',
                        style: TextStyle(fontWeight: FontWeight.w700),
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

  void _submit() {
    if (!_formKey.currentState!.validate() || _selectedType == null) return;
    context.read<RegistrationCubit>().createProperty(
      PropertyDraft(
        name: _nameController.text.trim(),
        propertyType: _selectedType!,
        sizeHectares: double.parse(
          _areaController.text.trim().replaceAll(',', '.'),
        ),
        cityState: _cityController.text.trim(),
      ),
    );
  }
}

class _FormSectionHeader extends StatelessWidget {
  const _FormSectionHeader({
    required this.icon,
    required this.title,
    required this.subtitle,
  });
  final IconData icon;
  final String title;
  final String subtitle;
  @override
  Widget build(BuildContext context) => Row(
    children: [
      Container(
        width: 36,
        height: 36,
        decoration: BoxDecoration(
          color: AppColors.figmaSoftGreen,
          borderRadius: BorderRadius.circular(10),
        ),
        child: Icon(icon, color: AppColors.figmaSecondary, size: 19),
      ),
      const SizedBox(width: 11),
      Expanded(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: const TextStyle(
                color: AppColors.figmaPrimary,
                fontSize: 15,
                fontWeight: FontWeight.w800,
                fontFamily: 'Poppins',
              ),
            ),
            Text(
              subtitle,
              style: const TextStyle(
                color: AppColors.figmaMuted,
                fontSize: 11.5,
              ),
            ),
          ],
        ),
      ),
    ],
  );
}

import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/widgets/labeled_text_field.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/core/widgets/signup_step_scaffold.dart';
import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_cubit.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_state.dart';
import 'package:ai_boi/features/registration/presentation/pages/signup_complete_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class SignupAddressPage extends StatefulWidget {
  const SignupAddressPage({super.key});

  @override
  State<SignupAddressPage> createState() => _SignupAddressPageState();
}

class _SignupAddressPageState extends State<SignupAddressPage> {
  final _formKey = GlobalKey<FormState>();
  final _cpfController = TextEditingController();
  final _cepController = TextEditingController();
  final _stateController = TextEditingController();
  final _neighborhoodController = TextEditingController();
  final _streetController = TextEditingController();
  final _numberController = TextEditingController();
  final _complementController = TextEditingController();

  @override
  void dispose() {
    for (final c in [
      _cpfController,
      _cepController,
      _stateController,
      _neighborhoodController,
      _streetController,
      _numberController,
      _complementController,
    ]) {
      c.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<RegistrationCubit, RegistrationState>(
      listener: (context, state) {
        if (state is RegistrationUserCreated) {
          final cubit = context.read<RegistrationCubit>();
          Navigator.pushAndRemoveUntil(
            context,
            MaterialPageRoute(
              builder: (_) => BlocProvider.value(
                value: cubit,
                child: const SignupCompletePage(),
              ),
            ),
            (route) => route.isFirst,
          );
        } else if (state is RegistrationError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message), backgroundColor: Colors.red),
          );
        }
      },
      builder: (context, state) {
        final isLoading = state is RegistrationLoading;
        return SignupSimpleScaffold(
          title: 'Seu endereço',
          subtitle:
              'Precisamos do seu endereço para concluir o cadastro no sistema.',
          child: Form(
            key: _formKey,
            child: Column(
              children: [
                LabeledTextField(
                  label: 'CPF',
                  hintText: '000.000.000-00',
                  controller: _cpfController,
                  keyboardType: TextInputType.number,
                  inputFormatters: [
                    FilteringTextInputFormatter.digitsOnly,
                    LengthLimitingTextInputFormatter(11),
                  ],
                  validator: (v) {
                    final digits = (v ?? '').replaceAll(RegExp(r'\D'), '');
                    if (digits.length != 11) return 'CPF deve ter 11 dígitos';
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                LabeledTextField(
                  label: 'CEP',
                  hintText: '00000-000',
                  controller: _cepController,
                  keyboardType: TextInputType.number,
                  validator: (v) =>
                      v == null || v.isEmpty ? 'Informe o CEP' : null,
                ),
                const SizedBox(height: 16),
                LabeledTextField(
                  label: 'Estado (UF)',
                  hintText: 'PA',
                  controller: _stateController,
                  maxLength: 2,
                  validator: (v) {
                    if (v == null || v.trim().isEmpty) return 'Informe o UF';
                    if (v.trim().length != 2) {
                      return 'Use 2 letras (ex: PA)';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                LabeledTextField(
                  label: 'Bairro',
                  hintText: 'Centro',
                  controller: _neighborhoodController,
                  validator: (v) =>
                      v == null || v.isEmpty ? 'Informe o bairro' : null,
                ),
                const SizedBox(height: 16),
                LabeledTextField(
                  label: 'Rua',
                  hintText: 'Rua principal',
                  controller: _streetController,
                  validator: (v) =>
                      v == null || v.isEmpty ? 'Informe a rua' : null,
                ),
                const SizedBox(height: 16),
                LabeledTextField(
                  label: 'Número',
                  hintText: '123',
                  controller: _numberController,
                  validator: (v) =>
                      v == null || v.isEmpty ? 'Informe o número' : null,
                ),
                const SizedBox(height: 16),
                LabeledTextField(
                  label: 'Complemento (opcional)',
                  hintText: 'Apto, bloco...',
                  controller: _complementController,
                ),
              ],
            ),
          ),
          bottom: PrimaryButton(
            text: isLoading ? 'Salvando...' : 'Concluir cadastro',
            onPressed: isLoading
                ? null
                : () {
                    if (_formKey.currentState!.validate()) {
                      final cubit = context.read<RegistrationCubit>();
                      cubit.cpf = _cpfController.text.replaceAll(RegExp(r'\D'), '');
                      cubit.completeRegistration(
                        AddressDraft(
                          zipCode: _cepController.text.trim(),
                          state: _stateController.text.trim(),
                          neighborhood: _neighborhoodController.text.trim(),
                          streetName: _streetController.text.trim(),
                          number: _numberController.text.trim(),
                          complement: _complementController.text.trim().isEmpty
                              ? null
                              : _complementController.text.trim(),
                        ),
                      );
                    }
                  },
          ),
        );
      },
    );
  }
}

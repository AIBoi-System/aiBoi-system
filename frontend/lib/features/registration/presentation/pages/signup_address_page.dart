import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/widgets/labeled_text_field.dart';
import 'package:ai_boi/core/widgets/primary_button.dart';
import 'package:ai_boi/core/widgets/signup_step_scaffold.dart';
import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';
import 'package:ai_boi/features/registration/domain/registration_validators.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_cubit.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_state.dart';
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
  final _nameController = TextEditingController();
  final _cpfController = TextEditingController();
  final _cepController = TextEditingController();
  final _stateController = TextEditingController();
  final _neighborhoodController = TextEditingController();
  final _streetController = TextEditingController();
  final _numberController = TextEditingController();
  final _complementController = TextEditingController();

  @override
  void initState() {
    super.initState();
    final cubit = context.read<RegistrationCubit>();
    _nameController.text = cubit.name;
    _cpfController.text = cubit.cpf;
  }

  @override
  void dispose() {
    for (final controller in [
      _nameController,
      _cpfController,
      _cepController,
      _stateController,
      _neighborhoodController,
      _streetController,
      _numberController,
      _complementController,
    ]) {
      controller.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BlocListener<RegistrationCubit, RegistrationState>(
      listener: (context, state) {
        if (state is RegistrationError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message), backgroundColor: Colors.red),
          );
        }
      },
      child: SignupStepScaffold(
        title: 'CPF e endereço',
        currentStep: 5,
        totalSteps: 6,
        bottom: PrimaryButton(text: 'Continuar', onPressed: _submit),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              LabeledTextField(
                label: 'Nome completo',
                hintText: 'Seu nome',
                controller: _nameController,
                validator: (value) =>
                    RegistrationValidators.requiredText(value, 'o nome'),
              ),
              const SizedBox(height: 16),
              LabeledTextField(
                label: 'CPF',
                hintText: '00000000000',
                controller: _cpfController,
                keyboardType: TextInputType.number,
                inputFormatters: [
                  FilteringTextInputFormatter.digitsOnly,
                  LengthLimitingTextInputFormatter(11),
                ],
                validator: RegistrationValidators.cpf,
              ),
              const SizedBox(height: 16),
              LabeledTextField(
                label: 'CEP',
                hintText: '00000000',
                controller: _cepController,
                keyboardType: TextInputType.number,
                inputFormatters: [
                  FilteringTextInputFormatter.digitsOnly,
                  LengthLimitingTextInputFormatter(8),
                ],
                validator: RegistrationValidators.zipCode,
              ),
              const SizedBox(height: 16),
              LabeledTextField(
                label: 'Estado (UF)',
                hintText: 'PA',
                controller: _stateController,
                maxLength: 2,
                validator: RegistrationValidators.state,
              ),
              const SizedBox(height: 16),
              LabeledTextField(
                label: 'Bairro',
                hintText: 'Centro',
                controller: _neighborhoodController,
                validator: (value) =>
                    RegistrationValidators.requiredText(value, 'o bairro'),
              ),
              const SizedBox(height: 16),
              LabeledTextField(
                label: 'Rua',
                hintText: 'Rua principal',
                controller: _streetController,
                validator: (value) =>
                    RegistrationValidators.requiredText(value, 'a rua'),
              ),
              const SizedBox(height: 16),
              LabeledTextField(
                label: 'Número',
                hintText: '123',
                controller: _numberController,
                validator: (value) =>
                    RegistrationValidators.requiredText(value, 'o número'),
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
      ),
    );
  }

  void _submit() {
    if (!_formKey.currentState!.validate()) return;
    final cubit = context.read<RegistrationCubit>();
    final ready = cubit.setProfile(
      name: _nameController.text,
      cpf: _cpfController.text,
      address: AddressDraft(
        zipCode: _cepController.text,
        state: _stateController.text,
        neighborhood: _neighborhoodController.text,
        streetName: _streetController.text,
        number: _numberController.text,
        complement: _complementController.text.isEmpty
            ? null
            : _complementController.text,
      ),
    );
    if (ready) {
      AppRouter.navigateRegistration(context, AppRouter.signupPassword);
    }
  }
}

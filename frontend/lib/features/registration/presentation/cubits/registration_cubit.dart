import 'package:ai_boi/core/network/api_exception.dart';
import 'package:ai_boi/features/auth/domain/repositories/auth_repository.dart';
import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';
import 'package:ai_boi/features/registration/domain/registration_validators.dart';
import 'package:ai_boi/features/registration/domain/repositories/registration_repository.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_state.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class RegistrationCubit extends Cubit<RegistrationState> {
  RegistrationCubit({
    required RegistrationRepository repository,
    required AuthRepository authRepository,
  }) : _repository = repository,
       _authRepository = authRepository,
       super(RegistrationInitial());

  final RegistrationRepository _repository;
  final AuthRepository _authRepository;

  String name = '';
  String email = '';
  String password = '';
  String cpf = '';
  String? phone;
  AddressDraft? address;
  RegistrationDraft? completedDraft;
  String? googleIdToken;
  bool emailVerified = false;
  bool phoneVerified = false;

  bool get canDefinePassword =>
      emailVerified && phoneVerified && cpf.isNotEmpty && address != null;

  void beginGoogleRegistration({
    required String email,
    required String name,
    required String idToken,
  }) {
    this.email = email.trim().toLowerCase();
    this.name = name.trim();
    googleIdToken = idToken;
    emailVerified = true;
    phoneVerified = false;
  }

  Future<void> sendVerificationCode() async {
    final validation = RegistrationValidators.email(email);
    if (validation != null) {
      emit(RegistrationError(validation));
      return;
    }
    email = email.trim().toLowerCase();
    emailVerified = false;
    await _run(() async {
      await _repository.sendVerificationCode(email);
      emit(RegistrationCodeSent());
    }, fallback: 'Não foi possível enviar o código de e-mail.');
  }

  Future<void> verifyCode(String code) async {
    await _run(() async {
      final verified = await _repository.verifyEmailCode(email, code);
      if (!verified) throw ApiException('Código de e-mail inválido.');
      emailVerified = true;
      emit(RegistrationEmailVerified());
    }, fallback: 'Não foi possível confirmar o e-mail.');
  }

  Future<void> sendPhoneVerificationCode(String value) async {
    final validation = RegistrationValidators.phone(value);
    if (validation != null) {
      emit(RegistrationError(validation));
      return;
    }
    phone = RegistrationValidators.digitsOnly(value);
    phoneVerified = false;
    await _run(() async {
      await _repository.sendPhoneVerificationCode(phone!);
      emit(RegistrationPhoneCodeSent());
    }, fallback: 'Não foi possível enviar o código por telefone.');
  }

  Future<void> verifyPhoneCode(String code) async {
    final currentPhone = phone;
    if (currentPhone == null) {
      emit(RegistrationError('Informe o telefone antes da confirmação.'));
      return;
    }
    await _run(() async {
      final verified = await _repository.verifyPhoneCode(currentPhone, code);
      if (!verified) throw ApiException('Código de telefone inválido.');
      phoneVerified = true;
      emit(RegistrationPhoneVerified());
    }, fallback: 'Não foi possível confirmar o telefone.');
  }

  bool setProfile({
    required String name,
    required String cpf,
    required AddressDraft address,
  }) {
    final error = _profileError(name: name, cpf: cpf, address: address);
    if (error != null) {
      emit(RegistrationError(error));
      return false;
    }
    this.name = name.trim();
    this.cpf = RegistrationValidators.digitsOnly(cpf);
    this.address = AddressDraft(
      zipCode: RegistrationValidators.digitsOnly(address.zipCode),
      state: address.state.trim().toUpperCase(),
      neighborhood: address.neighborhood.trim(),
      streetName: address.streetName.trim(),
      number: address.number.trim(),
      complement: address.complement?.trim(),
    );
    emit(RegistrationProfileReady());
    return true;
  }

  Future<void> completeRegistration() async {
    if (!canDefinePassword) {
      emit(
        RegistrationError(
          'Confirme e-mail e telefone e preencha seus dados antes da senha.',
        ),
      );
      return;
    }
    if (password.isEmpty) {
      emit(RegistrationError('Defina uma senha válida.'));
      return;
    }
    final draft = RegistrationDraft(
      name: name,
      email: email,
      password: password,
      cpf: cpf,
      phone: phone!,
      address: address!,
    );
    await _run(() async {
      final token = googleIdToken;
      final result = token == null
          ? await _repository.registerUser(draft)
          : await _repository.registerUserWithGoogle(draft, token);
      _adoptSession(result);
      password = '';
      completedDraft = result;
      emit(RegistrationUserCreated(result));
    }, fallback: 'Não foi possível concluir o cadastro.');
  }

  Future<void> createProperty(PropertyDraft property) async {
    var ownerId = completedDraft?.userId;
    var addressId = completedDraft?.userAddressId;
    emit(RegistrationLoading());
    try {
      if (ownerId == null || addressId == null) {
        final user = await _authRepository.getMe();
        ownerId = user['id_user'] as int?;
        addressId = user['address_id'] as int?;
      }
      if (ownerId == null || addressId == null) {
        emit(RegistrationError('Sessão expirada ou cadastro incompleto.'));
        return;
      }
      final created = await _repository.createProperty(
        ownerId: ownerId,
        addressId: addressId,
        property: property,
      );
      emit(RegistrationPropertyCreated(created));
    } catch (_) {
      emit(RegistrationError('Erro ao cadastrar propriedade.'));
    }
  }

  void _adoptSession(RegistrationDraft result) {
    final accessToken = result.accessToken;
    final refreshToken = result.refreshToken;
    final role = result.role;
    if (accessToken == null || refreshToken == null || role == null) {
      throw ApiException('Resposta de cadastro sem sessão válida.');
    }
    _authRepository.establishSession(
      accessToken: accessToken,
      refreshToken: refreshToken,
      role: role,
    );
  }

  String? _profileError({
    required String name,
    required String cpf,
    required AddressDraft address,
  }) {
    return RegistrationValidators.requiredText(name, 'o nome') ??
        RegistrationValidators.cpf(cpf) ??
        RegistrationValidators.zipCode(address.zipCode) ??
        RegistrationValidators.state(address.state) ??
        RegistrationValidators.requiredText(address.neighborhood, 'o bairro') ??
        RegistrationValidators.requiredText(address.streetName, 'a rua') ??
        RegistrationValidators.requiredText(address.number, 'o número');
  }

  Future<void> _run(
    Future<void> Function() action, {
    required String fallback,
  }) async {
    emit(RegistrationLoading());
    try {
      await action();
    } catch (error) {
      final message = error.toString().replaceFirst('Exception: ', '').trim();
      emit(RegistrationError(message.isEmpty ? fallback : message));
    }
  }
}

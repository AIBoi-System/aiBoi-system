import 'package:ai_boi/core/network/api_client.dart';
import 'package:ai_boi/features/auth/domain/repositories/auth_repository.dart';
import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';
import 'package:ai_boi/features/registration/domain/repositories/registration_repository.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_state.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class RegistrationCubit extends Cubit<RegistrationState> {
  RegistrationCubit({
    required RegistrationRepository repository,
    required AuthRepository authRepository,
    required ApiClient apiClient,
  })  : _repository = repository,
        _authRepository = authRepository,
        _apiClient = apiClient,
        super(RegistrationInitial());

  final RegistrationRepository _repository;
  final AuthRepository _authRepository;
  final ApiClient _apiClient;

  String name = '';
  String email = '';
  String password = '';
  String cpf = '';
  String? phone;
  RegistrationDraft? completedDraft;

  Future<void> sendVerificationCode() async {
    emit(RegistrationLoading());
    try {
      await _repository.sendVerificationCode(email);
      emit(RegistrationCodeSent());
    } catch (e) {
      final message = e.toString().replaceFirst('Exception: ', '');
      emit(RegistrationError(
        message.isNotEmpty
            ? message
            : 'Não foi possível enviar o código. Tente novamente.',
      ));
    }
  }

  Future<void> verifyCode(String code) async {
    emit(RegistrationLoading());
    try {
      final ok = await _repository.verifyEmailCode(email, code);
      if (ok) {
        emit(RegistrationEmailVerified());
      } else {
        emit(RegistrationError('Código inválido. Verifique e tente novamente.'));
      }
    } catch (e) {
      final message = e.toString().replaceFirst('Exception: ', '');
      emit(RegistrationError(
        message.isNotEmpty ? message : 'Erro ao verificar o código.',
      ));
    }
  }

  Future<void> completeRegistration(AddressDraft address) async {
    emit(RegistrationLoading());
    try {
      final draft = RegistrationDraft(
        name: name,
        email: email,
        password: password,
        cpf: cpf,
        phone: phone,
        address: address,
      );
      final result = await _repository.registerUser(draft);
      completedDraft = result;
      
      if (result.accessToken != null) {
        _apiClient.setAccessToken(result.accessToken);
      }

      emit(RegistrationUserCreated(result));
    } catch (e) {
      emit(RegistrationError(e.toString().replaceFirst('Exception: ', '')));
    }
  }

  Future<void> createProperty(PropertyDraft property) async {
    int? ownerId = completedDraft?.userId;
    int? addressId = completedDraft?.userAddressId;

    emit(RegistrationLoading());

    try {
      if (ownerId == null || addressId == null) {
        // Tenta obter do usuário logado se não estiver no fluxo de registro
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
    } catch (e) {
      emit(RegistrationError('Erro ao cadastrar propriedade.'));
    }
  }
}


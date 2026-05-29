import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';
import 'package:ai_boi/features/registration/domain/repositories/registration_repository.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_state.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class RegistrationCubit extends Cubit<RegistrationState> {
  RegistrationCubit({required RegistrationRepository repository})
      : _repository = repository,
        super(RegistrationInitial());

  final RegistrationRepository _repository;

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
      emit(RegistrationUserCreated(result));
    } catch (e) {
      emit(RegistrationError(e.toString().replaceFirst('Exception: ', '')));
    }
  }

  Future<void> createProperty(PropertyDraft property) async {
    final draft = completedDraft;
    if (draft?.userId == null || draft?.userAddressId == null) {
      emit(RegistrationError('Cadastro incompleto.'));
      return;
    }
    emit(RegistrationLoading());
    try {
      final created = await _repository.createProperty(
        ownerId: draft!.userId!,
        addressId: draft.userAddressId!,
        property: property,
      );
      emit(RegistrationPropertyCreated(created));
    } catch (e) {
      emit(RegistrationError('Erro ao cadastrar propriedade.'));
    }
  }
}

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:ai_boi/features/auth/domain/usecases/login_usecase.dart';
import 'login_state.dart';

class LoginCubit extends Cubit<LoginState> {
  LoginCubit({required LoginUseCase loginUseCase})
      : _loginUseCase = loginUseCase,
        super(LoginInitial());

  final LoginUseCase _loginUseCase;

  Future<void> fazerLogin(String email, String senha) async {
    emit(LoginLoading());

    try {
      await _loginUseCase(email: email, password: senha);
      emit(LoginSuccess());
    } on Exception catch (e) {
      final message = e.toString().replaceFirst('Exception: ', '');
      emit(LoginError(message));
    }
  }
}
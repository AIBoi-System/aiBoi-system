import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:ai_boi/features/auth/domain/usecases/login_usecase.dart';
import 'login_state.dart';

class LoginCubit extends Cubit<LoginState> {
  LoginCubit({required LoginUseCase loginUseCase})
      : _loginUseCase = loginUseCase,
        super(LoginInitial());

  final LoginUseCase _loginUseCase;

  Future<void> signIn(String email, String password) async {
    emit(LoginLoading());

    try {
      await _loginUseCase(email: email, password: password);
      emit(LoginSuccess());
    } on Exception catch (e) {
      final message = e.toString().replaceFirst('Exception: ', '');
      emit(LoginError(message));
    }
  }
}
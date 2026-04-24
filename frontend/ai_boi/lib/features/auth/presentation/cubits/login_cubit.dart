import 'package:flutter_bloc/flutter_bloc.dart';
import 'login_state.dart';

class LoginCubit extends Cubit<LoginState> {
  LoginCubit() : super(LoginInitial());

  Future<void> fazerLogin(String email, String senha) async {
    emit(LoginLoading());

    try {
      // Mock do tempo do servidor
      await Future.delayed(const Duration(seconds: 2));

      if (email == 'admin@fazenda.com' && senha == '123456') {
        emit(LoginSuccess());
      } else {
        emit(LoginError('E-mail ou senha inválidos.'));
      }
    } catch (e) {
      emit(LoginError('Erro de conexão.'));
    }
  }
}
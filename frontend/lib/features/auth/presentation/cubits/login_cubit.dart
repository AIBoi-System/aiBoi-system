import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:ai_boi/features/auth/domain/usecases/login_usecase.dart';
import 'package:ai_boi/features/auth/domain/repositories/auth_repository.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:flutter/foundation.dart';
import 'login_state.dart';

class LoginCubit extends Cubit<LoginState> {
  LoginCubit({
    required LoginUseCase loginUseCase,
    required AuthRepository authRepository,
  }) : _loginUseCase = loginUseCase,
       _authRepository = authRepository,
       super(LoginInitial());

  final LoginUseCase _loginUseCase;
  final AuthRepository _authRepository;

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

  Future<void> signInWithGoogle() async {
    const webClientId = String.fromEnvironment('GOOGLE_CLIENT_ID');
    if (kIsWeb && webClientId.isEmpty) {
      emit(
        LoginError(
          'Configure GOOGLE_CLIENT_ID para testar o login Google no navegador.',
        ),
      );
      return;
    }
    emit(LoginLoading());
    try {
      try {
        await GoogleSignIn.instance.signOut();
      } catch (_) {
        // Ignora erros ao deslogar
      }

      final googleUser = await GoogleSignIn.instance.authenticate();
      final GoogleSignInAuthentication googleAuth = googleUser.authentication;
      final String? idToken = googleAuth.idToken;

      if (idToken == null || idToken.isEmpty) {
        emit(LoginError('Não foi possível obter o token do Google.'));
        return;
      }

      final response = await _authRepository.loginWithGoogle(idToken: idToken);
      final needsRegistration =
          response['needs_registration'] as bool? ?? false;

      if (needsRegistration) {
        emit(
          GoogleLoginNeedsRegistration(
            email: response['email'] as String? ?? googleUser.email,
            name: response['name'] as String? ?? googleUser.displayName,
            idToken: idToken,
          ),
        );
      } else {
        emit(LoginSuccess());
      }
    } catch (e) {
      emit(LoginError(e.toString().replaceFirst('Exception: ', '')));
    }
  }
}

import 'package:ai_boi/features/auth/domain/entities/auth_session.dart';

abstract class AuthRepository {
  AuthSession? get session;

  bool get isAuthenticated;

  Future<void> login({required String email, required String password});

  Future<Map<String, dynamic>> loginWithGoogle({required String idToken});

  Future<Map<String, dynamic>> getMe();

  void establishSession({
    required String accessToken,
    required String refreshToken,
    required String role,
  });

  Future<void> refreshSession();

  Future<void> logout();
}

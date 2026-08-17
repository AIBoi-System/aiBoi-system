import 'package:ai_boi/features/auth/domain/entities/auth_session.dart';
import 'package:ai_boi/features/auth/domain/repositories/auth_repository.dart';

class MockAuthRepository implements AuthRepository {
  AuthSession? _session;

  @override
  AuthSession? get session => _session;

  @override
  bool get isAuthenticated => _session != null;

  @override
  Future<void> login({required String email, required String password}) async {
    await Future<void>.delayed(const Duration(milliseconds: 300));
    establishSession(
      accessToken: 'mock-access-token',
      refreshToken: 'mock-refresh-token',
      role: 'owner',
    );
  }

  @override
  Future<Map<String, dynamic>> loginWithGoogle({
    required String idToken,
  }) async {
    await Future<void>.delayed(const Duration(milliseconds: 300));
    establishSession(
      accessToken: 'mock-google-access-token',
      refreshToken: 'mock-google-refresh-token',
      role: 'owner',
    );
    return {
      'needs_registration': false,
      'access_token': session!.accessToken,
      'refresh_token': session!.refreshToken,
      'role': session!.role,
      'email': 'mockgoogle@test.com',
      'name': 'Mock Google User',
    };
  }

  @override
  void establishSession({
    required String accessToken,
    required String refreshToken,
    required String role,
  }) {
    _session = AuthSession(
      accessToken: accessToken,
      refreshToken: refreshToken,
      role: role,
    );
  }

  @override
  Future<void> refreshSession() async {
    if (_session == null) {
      throw StateError('No active session.');
    }
  }

  @override
  Future<void> logout() async {
    _session = null;
  }

  @override
  Future<Map<String, dynamic>> getMe() async {
    return {
      'id_user': 1,
      'email': 'mock@test.com',
      'name': 'Mock User',
      'address_id': 1,
    };
  }
}

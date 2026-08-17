import 'package:ai_boi/core/network/api_client.dart';

class AuthRemoteDataSource {
  AuthRemoteDataSource({required ApiClient apiClient}) : _api = apiClient;

  final ApiClient _api;

  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    return _api.post(
      '/auth/login',
      body: {'email': email.trim(), 'password': password},
    );
  }

  Future<Map<String, dynamic>> loginWithGoogle({
    required String idToken,
  }) async {
    return _api.post('/auth/login/google', body: {'id_token': idToken});
  }

  Future<Map<String, dynamic>> refresh(String refreshToken) {
    return _api.post('/auth/refresh', body: {'refresh_token': refreshToken});
  }

  Future<void> logout() async {
    await _api.post('/auth/logout');
  }

  Future<Map<String, dynamic>> getMe() async {
    return _api.get('/auth/me');
  }
}

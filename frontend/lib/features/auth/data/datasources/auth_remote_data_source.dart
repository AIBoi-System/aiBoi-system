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
}

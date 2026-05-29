import 'package:ai_boi/core/network/api_client.dart';
import 'package:ai_boi/core/network/api_exception.dart';
import 'package:ai_boi/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:ai_boi/features/auth/domain/repositories/auth_repository.dart';

class ApiAuthRepository implements AuthRepository {
  ApiAuthRepository({
    required AuthRemoteDataSource remote,
    required ApiClient apiClient,
  })  : _remote = remote,
        _apiClient = apiClient;

  final AuthRemoteDataSource _remote;
  final ApiClient _apiClient;

  String? _cachedToken;

  String? get accessToken => _cachedToken;

  @override
  Future<void> login({required String email, required String password}) async {
    try {
      final response = await _remote.login(email: email, password: password);
      final token = response['access_token'] as String?;
      if (token == null || token.isEmpty) {
        throw ApiException('Invalid login response.');
      }
      _cachedToken = token;
      _apiClient.setAccessToken(token);
    } on ApiException {
      rethrow;
    } catch (_) {
      throw ApiException('Unable to sign in. Check your connection.');
    }
  }
}

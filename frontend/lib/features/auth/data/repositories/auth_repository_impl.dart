import 'package:ai_boi/core/network/api_client.dart';
import 'package:ai_boi/core/network/api_exception.dart';
import 'package:ai_boi/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:ai_boi/features/auth/domain/entities/auth_session.dart';
import 'package:ai_boi/features/auth/domain/repositories/auth_repository.dart';

class AuthRepositoryImpl implements AuthRepository {
  AuthRepositoryImpl({
    required AuthRemoteDataSource remote,
    required ApiClient apiClient,
  }) : _remote = remote,
       _apiClient = apiClient;

  final AuthRemoteDataSource _remote;
  final ApiClient _apiClient;

  AuthSession? _session;

  @override
  AuthSession? get session => _session;

  @override
  bool get isAuthenticated => _session != null;

  @override
  Future<void> login({required String email, required String password}) async {
    try {
      final response = await _remote.login(email: email, password: password);
      _establishFromResponse(response);
    } on ApiException {
      rethrow;
    } catch (_) {
      throw ApiException('Unable to sign in. Check your connection.');
    }
  }

  @override
  Future<Map<String, dynamic>> loginWithGoogle({
    required String idToken,
  }) async {
    try {
      final response = await _remote.loginWithGoogle(idToken: idToken);
      final needsRegistration =
          response['needs_registration'] as bool? ?? false;
      if (!needsRegistration) {
        _establishFromResponse(response);
      }
      return response;
    } on ApiException {
      rethrow;
    } catch (_) {
      throw ApiException(
        'Unable to sign in with Google. Check your connection.',
      );
    }
  }

  @override
  void establishSession({
    required String accessToken,
    required String refreshToken,
    required String role,
  }) {
    if (accessToken.isEmpty || refreshToken.isEmpty) {
      throw ApiException('Invalid authentication response.');
    }
    _session = AuthSession(
      accessToken: accessToken,
      refreshToken: refreshToken,
      role: role,
    );
    _apiClient.setAccessToken(accessToken);
  }

  @override
  Future<void> refreshSession() async {
    final current = _session;
    if (current == null) {
      throw ApiException('No active session.');
    }
    try {
      final response = await _remote.refresh(current.refreshToken);
      _establishFromResponse(response);
    } catch (_) {
      _clearSession();
      rethrow;
    }
  }

  @override
  Future<void> logout() async {
    try {
      if (_session != null) {
        await _remote.logout();
      }
    } finally {
      _clearSession();
    }
  }

  @override
  Future<Map<String, dynamic>> getMe() => _remote.getMe();

  void _establishFromResponse(Map<String, dynamic> response) {
    final accessToken = response['access_token'] as String?;
    final refreshToken = response['refresh_token'] as String?;
    final role = response['role'] as String?;
    if (accessToken == null || refreshToken == null || role == null) {
      throw ApiException('Invalid authentication response.');
    }
    establishSession(
      accessToken: accessToken,
      refreshToken: refreshToken,
      role: role,
    );
  }

  void _clearSession() {
    _session = null;
    _apiClient.setAccessToken(null);
  }
}

import 'package:flutter/foundation.dart' show kIsWeb, TargetPlatform, defaultTargetPlatform;

/// API configuration (override via --dart-define).
class ApiConfig {
  ApiConfig._();

  /// Compile-time override (takes precedence if provided).
  static const String _envBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: '',
  );

  /// Runtime-aware base URL.
  /// - If API_BASE_URL is provided via --dart-define, use that.
  /// - On Web / Desktop / iOS: defaults to http://127.0.0.1:8001
  /// - On Android: defaults to http://10.0.2.2:8001 (emulator host loopback)
  static String get baseUrl {
    if (_envBaseUrl.isNotEmpty) return _envBaseUrl;
    if (!kIsWeb && defaultTargetPlatform == TargetPlatform.android) {
      return 'http://10.0.2.2:8001/api/v1';
    }
    return 'http://127.0.0.1:8001/api/v1';
  }

  static const bool useMockApi = bool.fromEnvironment(
    'USE_MOCK_API',
    defaultValue: false,
  );
}

/// API configuration (override via --dart-define).
class ApiConfig {
  ApiConfig._();

  /// Base URL without trailing slash.
  /// Android emulator: use http://10.0.2.2:8000
  /// iOS simulator / desktop: http://localhost:8000
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://localhost:8000',
  );

  static const bool useMockApi = bool.fromEnvironment(
    'USE_MOCK_API',
    defaultValue: false,
  );
}


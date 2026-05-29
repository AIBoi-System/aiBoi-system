import 'dart:convert';

import 'package:ai_boi/core/config/api_config.dart';
import 'package:ai_boi/core/network/api_exception.dart';
import 'package:http/http.dart' as http;

class ApiClient {
  ApiClient({http.Client? httpClient, String? baseUrl})
      : _http = httpClient ?? http.Client(),
        _baseUrl = baseUrl ?? ApiConfig.baseUrl;

  final http.Client _http;
  final String _baseUrl;

  String? _accessToken;

  void setAccessToken(String? token) {
    _accessToken = token;
  }

  Map<String, String> get _headers {
    final headers = <String, String>{
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    if (_accessToken != null) {
      headers['Authorization'] = 'Bearer $_accessToken';
    }
    return headers;
  }

  Future<Map<String, dynamic>> post(
    String path, {
    Map<String, dynamic>? body,
  }) async {
    final response = await _http.post(
      Uri.parse('$_baseUrl$path'),
      headers: _headers,
      body: jsonEncode(body ?? {}),
    );
    return _parseResponse(response);
  }

  Future<Map<String, dynamic>> get(String path) async {
    final response = await _http.get(
      Uri.parse('$_baseUrl$path'),
      headers: _headers,
    );
    return _parseResponse(response);
  }

  Map<String, dynamic> _parseResponse(http.Response response) {
    Map<String, dynamic>? data;
    if (response.body.isNotEmpty) {
      final decoded = jsonDecode(response.body);
      if (decoded is Map<String, dynamic>) {
        data = decoded;
      }
    }

    if (response.statusCode >= 200 && response.statusCode < 300) {
      return data ?? {};
    }

    final detail = data?['detail'];
    String message;
    if (detail is String) {
      message = detail;
    } else if (detail is List && detail.isNotEmpty) {
      message = detail.first['msg']?.toString() ?? 'Request failed';
    } else {
      message = 'Request failed (${response.statusCode})';
    }
    throw ApiException(message, statusCode: response.statusCode);
  }

  void dispose() {
    _http.close();
  }
}

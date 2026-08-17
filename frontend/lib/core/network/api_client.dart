import 'dart:async';
import 'dart:convert';

import 'package:ai_boi/core/config/api_config.dart';
import 'package:ai_boi/core/network/api_exception.dart';
import 'package:http/http.dart' as http;

class ApiClient {
  static const _requestTimeout = Duration(seconds: 15);

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
    try {
      final response = await _http.post(
        Uri.parse('$_baseUrl$path'),
        headers: _headers,
        body: jsonEncode(body ?? {}),
      ).timeout(_requestTimeout);
      final data = _handleResponse(response);
      return data is Map<String, dynamic> ? data : {};
    } on TimeoutException {
      throw ApiException('Request timeout', statusCode: 408);
    }
  }

  Future<Map<String, dynamic>> get(String path) async {
    try {
      final response = await _http.get(
        Uri.parse('$_baseUrl$path'),
        headers: _headers,
      ).timeout(_requestTimeout);
      final data = _handleResponse(response);
      return data is Map<String, dynamic> ? data : {};
    } on TimeoutException {
      throw ApiException('Request timeout', statusCode: 408);
    }
  }

  Future<List<dynamic>> getList(String path) async {
    try {
      final response = await _http.get(
        Uri.parse('$_baseUrl$path'),
        headers: _headers,
      ).timeout(_requestTimeout);
      final data = _handleResponse(response);
      if (data is List) return data;
      return [];
    } on TimeoutException {
      throw ApiException('Request timeout', statusCode: 408);
    }
  }

  Future<Map<String, dynamic>> put(
    String path, {
    required Map<String, dynamic> body,
  }) async {
    try {
      final response = await _http.put(
        Uri.parse('$_baseUrl$path'),
        headers: _headers,
        body: jsonEncode(body),
      ).timeout(_requestTimeout);
      final data = _handleResponse(response);
      return data is Map<String, dynamic> ? data : {};
    } on TimeoutException {
      throw ApiException('Request timeout', statusCode: 408);
    }
  }

  dynamic _handleResponse(http.Response response) {
    dynamic data;
    if (response.body.isNotEmpty) {
      try {
        data = jsonDecode(response.body);
      } catch (e) {
        // Non-JSON response body — keep raw text for debugging
        data = {'_raw_body': response.body};
      }
    }

    if (response.statusCode >= 200 && response.statusCode < 300) {
      return data;
    }

    String message = 'Request failed (${response.statusCode})';
    if (data is Map) {
      final detail = data['detail'];
      if (detail is String) {
        message = detail;
      } else if (detail is List && detail.isNotEmpty) {
        message = detail.first['msg']?.toString() ?? message;
      }
    }

    throw ApiException(message, statusCode: response.statusCode);
  }

  void dispose() {
    _http.close();
  }
}

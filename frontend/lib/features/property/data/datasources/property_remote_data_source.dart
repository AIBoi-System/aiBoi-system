import 'package:ai_boi/core/network/api_client.dart';
import 'package:ai_boi/core/network/api_endpoints.dart';
import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';

class PropertyRemoteDataSource {
  PropertyRemoteDataSource({required ApiClient apiClient}) : _api = apiClient;

  final ApiClient _api;

  Future<List<RegisteredProperty>> listProperties() async {
    final rows = await _api.getList(ApiEndpoints.properties);
    return rows.map((row) => _mapProperty(row as Map<String, dynamic>)).toList();
  }

  Future<RegisteredProperty> getProperty(int id) async {
    final response = await _api.get(ApiEndpoints.propertyById(id));
    return _mapProperty(response);
  }

  RegisteredProperty _mapProperty(Map<String, dynamic> row) {
    final type = row['property_type']?.toString() ?? '';
    return RegisteredProperty(
      id: row['id_property'] as int? ?? 0,
      name: row['name']?.toString() ?? '',
      cityState: '—',
      purpose: _propertyTypeLabel(type),
      hectares: (row['area'] as num?)?.toDouble() ?? 0,
      ownerId: row['owner_id'] as int?,
      addressId: row['address_id'] as int?,
    );
  }

  String _propertyTypeLabel(String apiType) {
    switch (apiType.toUpperCase()) {
      case 'DAIRY':
        return 'Leite';
      case 'BEEF':
        return 'Corte';
      case 'MIXED':
        return 'Mista';
      case 'REARING':
        return 'Recria';
      case 'FEEDLOT':
        return 'Confinamento';
      case 'SEMI_FEEDLOT':
        return 'Semi-confinamento';
      default:
        return apiType;
    }
  }
}

import 'package:ai_boi/core/network/api_client.dart';
import 'package:ai_boi/core/network/api_endpoints.dart';

class OperationsRemoteDataSource {
  OperationsRemoteDataSource({required ApiClient apiClient}) : _api = apiClient;

  final ApiClient _api;

  Future<Object?> listAnimals({required int propertyId}) =>
      _api.getList('${ApiEndpoints.animals}?property_id=$propertyId');

  Future<Object?> listBatches({required int propertyId}) =>
      _api.getList('${ApiEndpoints.batches}?property_id=$propertyId');

  Future<Object?> listReproductions({required int propertyId}) =>
      _api.getList('${ApiEndpoints.reproductions}?property_id=$propertyId');

  Future<Object?> listHealthRecords({required int propertyId}) =>
      _api.getList('${ApiEndpoints.health}?property_id=$propertyId');

  Future<Object?> listPastures({int? propertyId}) {
    final path = propertyId != null
        ? ApiEndpoints.pasturesByProperty(propertyId)
        : ApiEndpoints.pastures;
    return _api.getList(path);
  }

  Future<Object?> listPaddocks({int? propertyId}) {
    final path = propertyId != null
        ? ApiEndpoints.paddocksByProperty(propertyId)
        : ApiEndpoints.paddocks;
    return _api.getList(path);
  }

  Future<Object?> listWeighingsByAnimal(int animalId, {required int propertyId}) =>
      _api.getList('${ApiEndpoints.weighingsByAnimal(animalId)}?property_id=$propertyId');

  Future<Map<String, dynamic>> createWeighing(
    Map<String, dynamic> body, {
    required int propertyId,
  }) =>
      _api.post('${ApiEndpoints.weighings}?property_id=$propertyId', body: body);

  Future<Map<String, dynamic>> registerBirth(
    int reproductionId,
    Map<String, dynamic> body,
  ) => _api.post(ApiEndpoints.reproductionBirth(reproductionId), body: body);

  Future<Object?> listOwnerModules(int ownerId) =>
      _api.getList(ApiEndpoints.ownerModulesByOwner(ownerId));

  Future<Map<String, dynamic>> getDashboard(int propertyId) async {
    return _api.get(ApiEndpoints.dashboard(propertyId));
  }

  Future<Map<String, dynamic>> createHealthRecord(
    Map<String, dynamic> body, {
    required int propertyId,
  }) =>
      _api.post('${ApiEndpoints.health}?property_id=$propertyId', body: body);

  Future<Map<String, dynamic>> createReproduction(
    int propertyId,
    Map<String, dynamic> body,
  ) => _api.post(
    '${ApiEndpoints.reproductions}?property_id=$propertyId',
    body: body,
  );

  Future<Map<String, dynamic>> createPasture(
    Map<String, dynamic> body, {
    required int propertyId,
  }) =>
      _api.post('${ApiEndpoints.pastures}?property_id=$propertyId', body: body);

  Future<Map<String, dynamic>> createPaddock(
    Map<String, dynamic> body, {
    required int propertyId,
  }) =>
      _api.post('${ApiEndpoints.paddocks}?property_id=$propertyId', body: body);

  Future<Map<String, dynamic>> createBatch(
    Map<String, dynamic> body, {
    required int propertyId,
  }) =>
      _api.post('${ApiEndpoints.batches}?property_id=$propertyId', body: body);

  Future<Map<String, dynamic>> updateAnimal(
    int id,
    int propertyId,
    Map<String, dynamic> body,
  ) => _api.put(
    '${ApiEndpoints.animals}$id?property_id=$propertyId',
    body: body,
  );
}

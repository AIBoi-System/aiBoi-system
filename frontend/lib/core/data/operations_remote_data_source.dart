import 'package:ai_boi/core/network/api_client.dart';
import 'package:ai_boi/core/network/api_endpoints.dart';

class OperationsRemoteDataSource {
  OperationsRemoteDataSource({required ApiClient apiClient}) : _api = apiClient;

  final ApiClient _api;

  Future<Object?> listAnimals() =>
      _api.getList(ApiEndpoints.animals);

  Future<Object?> listBatches() =>
      _api.getList(ApiEndpoints.batches);

  Future<Object?> listReproductions() =>
      _api.getList(ApiEndpoints.reproductions);

  Future<Object?> listHealthRecords() =>
      _api.getList(ApiEndpoints.health);

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

  Future<Object?> listWeighingsByAnimal(int animalId) =>
      _api.getList(ApiEndpoints.weighingsByAnimal(animalId));

  Future<Map<String, dynamic>> createWeighing(Map<String, dynamic> body) =>
      _api.post(ApiEndpoints.weighings, body: body);

  Future<Map<String, dynamic>> registerBirth(
    int reproductionId,
    Map<String, dynamic> body,
  ) =>
      _api.post(ApiEndpoints.reproductionBirth(reproductionId), body: body);

  Future<Object?> listOwnerModules(int ownerId) =>
      _api.getList(ApiEndpoints.ownerModulesByOwner(ownerId));
}


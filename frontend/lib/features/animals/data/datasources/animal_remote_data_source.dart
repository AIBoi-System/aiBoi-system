import 'package:ai_boi/core/network/api_client.dart';
import 'package:ai_boi/core/network/api_endpoints.dart';
import '../models/animal_model.dart';

class AnimalRemoteDataSource {
  AnimalRemoteDataSource({
    required ApiClient apiClient,
  }) : _api = apiClient;

  final ApiClient _api;

  Future<List<AnimalModel>> listAnimals(int propertyId) async {
    final rows = await _api.getList(
      '${ApiEndpoints.animals}?property_id=$propertyId',
    );

    return rows
        .map(
          (row) => AnimalModel.fromJson(
            row as Map<String, dynamic>,
          ),
        )
        .toList();
  }

  Future<AnimalModel> getAnimal(int id, int propertyId) async {
    final response = await _api.get(
      '${ApiEndpoints.animals}$id?property_id=$propertyId',
    );

    return AnimalModel.fromJson(response);
  }

  Future<AnimalModel> createAnimal(
    AnimalModel animal,
    int propertyId,
  ) async {
    final response = await _api.post(
      '${ApiEndpoints.animals}?property_id=$propertyId',
      body: animal.toJson(),
    );

    return AnimalModel.fromJson(response);
  }

  Future<AnimalModel> updateAnimal(
    int id,
    AnimalModel animal,
    int propertyId,
  ) async {
    final response = await _api.put(
      '${ApiEndpoints.animals}$id?property_id=$propertyId',
      body: animal.toJson(),
    );

    return AnimalModel.fromJson(response);
  }

  Future<List<dynamic>> listBatches() async {
    return await _api.getList(ApiEndpoints.batches);
  }
}

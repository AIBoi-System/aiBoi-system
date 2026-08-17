import '../../domain/entities/animal.dart';
import '../../domain/repositories/animal_repository.dart';
import '../datasources/animal_remote_data_source.dart';
import '../models/animal_model.dart';

class AnimalRepositoryImpl implements AnimalRepository {
  final AnimalRemoteDataSource remoteDataSource;

  AnimalRepositoryImpl(this.remoteDataSource);

  @override
  Future<List<Animal>> listAnimals(int propertyId) async {
    return await remoteDataSource.listAnimals(propertyId);
  }

  @override
  Future<Animal> getAnimal(int id, int propertyId) async {
    return await remoteDataSource.getAnimal(id, propertyId);
  }

  @override
  Future<Animal> createAnimal(Animal animal, int propertyId) async {
    final model = AnimalModel(
      id: animal.id,
      identificationNumber: animal.identificationNumber,
      name: animal.name,
      sex: animal.sex,
      breed: animal.breed,
      category: animal.category,
      lifeStatus: animal.lifeStatus,
      reproductiveStatus: animal.reproductiveStatus,
      birthDate: animal.birthDate,
      origin: animal.origin,
      batchId: animal.batchId,
      notes: animal.notes,
      birthWeight: animal.birthWeight,
      weaningWeight: animal.weaningWeight,
      entryDate: animal.entryDate,
      pedigreePo: animal.pedigreePo,
    );
    return await remoteDataSource.createAnimal(model, propertyId);
  }

  @override
  Future<Animal> updateAnimal(int id, Animal animal, int propertyId) async {
    final model = AnimalModel(
      id: animal.id,
      identificationNumber: animal.identificationNumber,
      name: animal.name,
      sex: animal.sex,
      breed: animal.breed,
      category: animal.category,
      lifeStatus: animal.lifeStatus,
      reproductiveStatus: animal.reproductiveStatus,
      birthDate: animal.birthDate,
      origin: animal.origin,
      batchId: animal.batchId,
      notes: animal.notes,
      birthWeight: animal.birthWeight,
      weaningWeight: animal.weaningWeight,
      entryDate: animal.entryDate,
      pedigreePo: animal.pedigreePo,
    );
    return await remoteDataSource.updateAnimal(id, model, propertyId);
  }
}

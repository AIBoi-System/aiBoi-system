import '../../domain/entities/animal.dart';
import '../../domain/repositories/animal_repository.dart';
import '../datasources/animal_remote_data_source.dart';
import '../models/animal_model.dart';

class AnimalRepositoryImpl implements AnimalRepository {
  final AnimalRemoteDataSource remoteDataSource;

  AnimalRepositoryImpl(this.remoteDataSource);

  @override
  Future<List<Animal>> listAnimals() async {
    return await remoteDataSource.listAnimals();
  }

  @override
  Future<Animal> getAnimal(int id) async {
    return await remoteDataSource.getAnimal(id);
  }

  @override
  Future<Animal> createAnimal(Animal animal) async {
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
    return await remoteDataSource.createAnimal(model);
  }

  @override
  Future<Animal> updateAnimal(int id, Animal animal) async {
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
    return await remoteDataSource.updateAnimal(id, model);
  }
}

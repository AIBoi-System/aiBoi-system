import '../entities/animal.dart';

abstract class AnimalRepository {
  Future<List<Animal>> listAnimals(int propertyId);
  Future<Animal> getAnimal(int id, int propertyId);
  Future<Animal> createAnimal(Animal animal, int propertyId);
  Future<Animal> updateAnimal(int id, Animal animal, int propertyId);
}


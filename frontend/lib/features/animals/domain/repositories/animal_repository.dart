import '../entities/animal.dart';

abstract class AnimalRepository {
  Future<List<Animal>> listAnimals();
  Future<Animal> getAnimal(int id);
  Future<Animal> createAnimal(Animal animal);
  Future<Animal> updateAnimal(int id, Animal animal);
}

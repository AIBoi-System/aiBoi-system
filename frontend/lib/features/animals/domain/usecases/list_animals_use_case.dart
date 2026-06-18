import '../entities/animal.dart';
import '../repositories/animal_repository.dart';

class ListAnimalsUseCase {
  final AnimalRepository repository;

  ListAnimalsUseCase(this.repository);

  Future<List<Animal>> call() async {
    return await repository.listAnimals();
  }
}

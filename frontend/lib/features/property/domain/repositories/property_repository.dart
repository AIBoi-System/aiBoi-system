import '../../../registration/domain/entities/registration_draft.dart';

abstract class PropertyRepository {
  Future<List<RegisteredProperty>> listProperties();
  Future<RegisteredProperty> getProperty(int id);
}

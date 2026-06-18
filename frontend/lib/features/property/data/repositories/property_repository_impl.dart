import '../../../registration/domain/entities/registration_draft.dart';
import '../../domain/repositories/property_repository.dart';
import '../datasources/property_remote_data_source.dart';

class PropertyRepositoryImpl implements PropertyRepository {
  final PropertyRemoteDataSource remoteDataSource;

  PropertyRepositoryImpl(this.remoteDataSource);

  @override
  Future<List<RegisteredProperty>> listProperties() async {
    return await remoteDataSource.listProperties();
  }

  @override
  Future<RegisteredProperty> getProperty(int id) async {
    return await remoteDataSource.getProperty(id);
  }
}

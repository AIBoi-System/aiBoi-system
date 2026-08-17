import 'package:ai_boi/core/config/api_config.dart';
import 'package:ai_boi/core/network/api_client.dart';
import 'package:ai_boi/features/animals/data/datasources/animal_remote_data_source.dart';
import 'package:ai_boi/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:ai_boi/features/auth/data/repositories/auth_repository_impl.dart';
import 'package:ai_boi/features/auth/data/repositories/mock_auth_repository.dart';
import 'package:ai_boi/features/auth/domain/repositories/auth_repository.dart';
import 'package:ai_boi/features/auth/domain/usecases/login_usecase.dart';
import 'package:ai_boi/features/auth/presentation/cubits/login_cubit.dart';
import 'package:ai_boi/features/registration/data/datasources/registration_remote_data_source.dart';
import 'package:ai_boi/features/registration/data/repositories/registration_repository_impl.dart';
import 'package:ai_boi/features/registration/data/repositories/mock_registration_repository.dart';
import 'package:ai_boi/features/registration/domain/repositories/registration_repository.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_cubit.dart';
import 'package:ai_boi/features/property/data/datasources/property_remote_data_source.dart';
import 'package:ai_boi/features/property/data/repositories/property_repository_impl.dart';
import 'package:ai_boi/features/property/domain/repositories/property_repository.dart';

import 'package:ai_boi/core/data/operations_remote_data_source.dart';
import 'package:ai_boi/features/dashboard/presentation/cubits/dashboard_cubit.dart';

class AppBindings {
  static final ApiClient _apiClient = ApiClient();

  static AuthRepository _createAuthRepository() {
    if (ApiConfig.useMockApi) {
      return MockAuthRepository();
    }
    return AuthRepositoryImpl(
      remote: AuthRemoteDataSource(apiClient: _apiClient),
      apiClient: _apiClient,
    );
  }

  static final AuthRepository authRepository = _createAuthRepository();

  static RegistrationRepository _registrationRepository() {
    if (ApiConfig.useMockApi) {
      return MockRegistrationRepository();
    }
    return RegistrationRepositoryImpl(
      remote: RegistrationRemoteDataSource(apiClient: _apiClient),
    );
  }

  static LoginCubit createLoginCubit() {
    return LoginCubit(
      loginUseCase: LoginUseCase(authRepository),
      authRepository: authRepository,
    );
  }

  static RegistrationCubit createRegistrationCubit() {
    return RegistrationCubit(
      repository: _registrationRepository(),
      authRepository: authRepository,
    );
  }

  static PropertyRepository propertyRepository() {
    return PropertyRepositoryImpl(
      PropertyRemoteDataSource(apiClient: _apiClient),
    );
  }

  static AnimalRemoteDataSource animalRemote() {
    return AnimalRemoteDataSource(apiClient: _apiClient);
  }

  static OperationsRemoteDataSource operations() {
    return OperationsRemoteDataSource(apiClient: _apiClient);
  }

  static DashboardCubit createDashboardCubit() {
    return DashboardCubit(operations: operations());
  }
}

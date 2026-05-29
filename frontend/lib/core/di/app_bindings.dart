import 'package:ai_boi/core/config/api_config.dart';
import 'package:ai_boi/core/network/api_client.dart';
import 'package:ai_boi/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:ai_boi/features/auth/data/repositories/api_auth_repository.dart';
import 'package:ai_boi/features/auth/data/repositories/mock_auth_repository.dart';
import 'package:ai_boi/features/auth/domain/repositories/auth_repository.dart';
import 'package:ai_boi/features/auth/domain/usecases/login_usecase.dart';
import 'package:ai_boi/features/auth/presentation/cubits/login_cubit.dart';
import 'package:ai_boi/features/registration/data/datasources/registration_remote_data_source.dart';
import 'package:ai_boi/features/registration/data/repositories/api_registration_repository.dart';
import 'package:ai_boi/features/registration/data/repositories/mock_registration_repository.dart';
import 'package:ai_boi/features/registration/domain/repositories/registration_repository.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_cubit.dart';

class AppBindings {
  static final ApiClient _apiClient = ApiClient();

  static AuthRepository _authRepository() {
    if (ApiConfig.useMockApi) {
      return MockAuthRepository();
    }
    return ApiAuthRepository(
      remote: AuthRemoteDataSource(apiClient: _apiClient),
      apiClient: _apiClient,
    );
  }

  static RegistrationRepository _registrationRepository() {
    if (ApiConfig.useMockApi) {
      return MockRegistrationRepository();
    }
    return ApiRegistrationRepository(
      remote: RegistrationRemoteDataSource(apiClient: _apiClient),
    );
  }

  static LoginCubit createLoginCubit() {
    return LoginCubit(loginUseCase: LoginUseCase(_authRepository()));
  }

  static RegistrationCubit createRegistrationCubit() {
    return RegistrationCubit(repository: _registrationRepository());
  }
}

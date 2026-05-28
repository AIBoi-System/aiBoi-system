import 'package:ai_boi/features/auth/data/repositories/mock_auth_repository.dart';
import 'package:ai_boi/features/auth/domain/usecases/login_usecase.dart';
import 'package:ai_boi/features/auth/presentation/cubits/login_cubit.dart';
import 'package:ai_boi/features/registration/data/repositories/mock_registration_repository.dart';
import 'package:ai_boi/features/registration/presentation/cubits/registration_cubit.dart';

class AppBindings {
  static LoginCubit createLoginCubit() {
    final repository = MockAuthRepository();
    final loginUseCase = LoginUseCase(repository);
    return LoginCubit(loginUseCase: loginUseCase);
  }

  static RegistrationCubit createRegistrationCubit() {
    return RegistrationCubit(
      repository: MockRegistrationRepository(),
    );
  }
}

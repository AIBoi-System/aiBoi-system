import 'package:ai_boi/features/auth/domain/repositories/auth_repository.dart';

class MockAuthRepository implements AuthRepository {
  @override
  Future<void> login({
    required String email,
    required String password,
  }) async {
    await Future.delayed(const Duration(seconds: 2));

    if (email == 'admin@fazenda.com' && password == '123456') {
      return;
    }

    throw Exception('E-mail ou senha inválidos.');
  }
}

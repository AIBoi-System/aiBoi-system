import '../../domain/repositories/auth_repository.dart';

class MockAuthRepository implements AuthRepository {
  @override
  Future<void> login({required String email, required String password}) async {
    await Future.delayed(const Duration(seconds: 1));
  }

  @override
  Future<Map<String, dynamic>> getMe() async {
    return {
      'id_user': 1,
      'email': 'mock@test.com',
      'name': 'Mock User',
      'address_id': 1,
    };
  }
}

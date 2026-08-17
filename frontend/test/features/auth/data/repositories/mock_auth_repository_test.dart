import 'package:ai_boi/features/auth/data/repositories/mock_auth_repository.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('keeps tokens in memory and clears them on logout', () async {
    final repository = MockAuthRepository();

    repository.establishSession(
      accessToken: 'access',
      refreshToken: 'refresh',
      role: 'owner',
    );

    expect(repository.isAuthenticated, isTrue);
    expect(repository.session?.refreshToken, 'refresh');

    await repository.logout();

    expect(repository.isAuthenticated, isFalse);
    expect(repository.session, isNull);
  });
}

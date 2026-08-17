import 'package:ai_boi/features/registration/domain/registration_validators.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('RegistrationValidators.cpf', () {
    test('accepts a CPF with valid check digits', () {
      expect(RegistrationValidators.cpf('529.982.247-25'), isNull);
    });

    test('rejects invalid and repeated CPFs', () {
      expect(RegistrationValidators.cpf('529.982.247-24'), isNotNull);
      expect(RegistrationValidators.cpf('111.111.111-11'), isNotNull);
    });
  });

  test('requires an eight digit CEP', () {
    expect(RegistrationValidators.zipCode('01001-000'), isNull);
    expect(RegistrationValidators.zipCode('0100100'), isNotNull);
  });

  test('accepts only official Brazilian states', () {
    expect(RegistrationValidators.state('sp'), isNull);
    expect(RegistrationValidators.state('AA'), isNotNull);
  });

  test('requires a valid Brazilian area code and phone length', () {
    expect(RegistrationValidators.phone('(11) 99999-9999'), isNull);
    expect(RegistrationValidators.phone('(10) 99999-9999'), isNotNull);
    expect(RegistrationValidators.phone('119999999'), isNotNull);
  });
}

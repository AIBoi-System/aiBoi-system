import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';
import 'package:ai_boi/features/registration/domain/repositories/registration_repository.dart';

class MockRegistrationRepository implements RegistrationRepository {
  static const String mockCode = '12345';
  final Set<String> _verifiedEmails = {};
  final Set<String> _verifiedPhones = {};
  int _userSequence = 1;
  int _propertySequence = 1;

  @override
  Future<void> sendVerificationCode(String email) async {
    await Future<void>.delayed(const Duration(milliseconds: 300));
    _verifiedEmails.remove(email);
  }

  @override
  Future<bool> verifyEmailCode(String email, String code) async {
    await Future<void>.delayed(const Duration(milliseconds: 300));
    if (code != mockCode) return false;
    _verifiedEmails.add(email);
    return true;
  }

  @override
  Future<void> sendPhoneVerificationCode(String phone) async {
    await Future<void>.delayed(const Duration(milliseconds: 300));
    _verifiedPhones.remove(phone);
  }

  @override
  Future<bool> verifyPhoneCode(String phone, String code) async {
    await Future<void>.delayed(const Duration(milliseconds: 300));
    if (code != mockCode) return false;
    _verifiedPhones.add(phone);
    return true;
  }

  @override
  Future<RegistrationDraft> registerUser(RegistrationDraft draft) async {
    await Future<void>.delayed(const Duration(milliseconds: 400));
    if (!_verifiedEmails.contains(draft.email)) {
      throw Exception('E-mail não verificado.');
    }
    if (!_verifiedPhones.contains(draft.phone)) {
      throw Exception('Telefone não verificado.');
    }
    return draft.copyWith(
      userId: _userSequence++,
      userAddressId: 100 + _userSequence,
      accessToken: 'mock-access-token',
      refreshToken: 'mock-refresh-token',
      role: 'owner',
    );
  }

  @override
  Future<RegistrationDraft> registerUserWithGoogle(
    RegistrationDraft draft,
    String idToken,
  ) async {
    await Future<void>.delayed(const Duration(milliseconds: 400));
    if (!_verifiedPhones.contains(draft.phone)) {
      throw Exception('Telefone não verificado.');
    }
    return draft.copyWith(
      userId: _userSequence++,
      userAddressId: 100 + _userSequence,
      accessToken: 'mock-google-access-token',
      refreshToken: 'mock-google-refresh-token',
      role: 'owner',
    );
  }

  @override
  Future<RegisteredProperty> createProperty({
    required int ownerId,
    required int addressId,
    required PropertyDraft property,
  }) async {
    await Future<void>.delayed(const Duration(milliseconds: 300));
    return RegisteredProperty(
      id: _propertySequence++,
      name: property.name,
      cityState: property.cityState,
      purpose: property.propertyType,
      hectares: property.sizeHectares,
    );
  }
}

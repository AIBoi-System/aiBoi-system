import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';
import 'package:ai_boi/features/registration/domain/repositories/registration_repository.dart';

class MockRegistrationRepository implements RegistrationRepository {
  static const String mockCode = '12345';
  final Set<String> _verifiedEmails = {};
  int _userSeq = 1;
  int _propertySeq = 1;

  @override
  Future<void> sendVerificationCode(String email) async {
    await Future.delayed(const Duration(milliseconds: 600));
    _verifiedEmails.remove(email);
  }

  @override
  Future<bool> verifyEmailCode(String email, String code) async {
    await Future.delayed(const Duration(milliseconds: 500));
    if (code == mockCode) {
      _verifiedEmails.add(email);
      return true;
    }
    return false;
  }

  @override
  Future<RegistrationDraft> registerUser(RegistrationDraft draft) async {
    await Future.delayed(const Duration(milliseconds: 800));
    if (!_verifiedEmails.contains(draft.email)) {
      throw Exception('E-mail não verificado.');
    }
    return draft.copyWith(
      userId: _userSeq++,
      userAddressId: 100 + _userSeq,
    );
  }

  @override
  Future<RegisteredProperty> createProperty({
    required int ownerId,
    required int addressId,
    required PropertyDraft property,
  }) async {
    await Future.delayed(const Duration(milliseconds: 700));
    return RegisteredProperty(
      id: _propertySeq++,
      name: property.name,
      cityState: property.cityState,
      purpose: property.propertyType,
      hectares: property.sizeHectares,
    );
  }
}

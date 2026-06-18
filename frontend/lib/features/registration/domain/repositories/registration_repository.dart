import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';

abstract class RegistrationRepository {
  Future<void> sendVerificationCode(String email);
  Future<bool> verifyEmailCode(String email, String code);
  Future<RegistrationDraft> registerUser(RegistrationDraft draft);
  Future<RegisteredProperty> createProperty({
    required int ownerId,
    required int addressId,
    required PropertyDraft property,
  });
}


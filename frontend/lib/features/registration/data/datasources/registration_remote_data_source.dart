import 'package:ai_boi/core/network/api_client.dart';
import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';

class RegistrationRemoteDataSource {
  RegistrationRemoteDataSource({required ApiClient apiClient})
      : _api = apiClient;

  final ApiClient _api;

  Future<void> sendVerificationCode(String email) async {
    await _api.post('/auth/signup/send-code', body: {'email': email.trim()});
  }

  Future<void> verifyEmailCode(String email, String code) async {
    await _api.post(
      '/auth/signup/verify-code',
      body: {'email': email.trim(), 'code': code},
    );
  }

  Future<Map<String, dynamic>> registerUser(RegistrationDraft draft) async {
    return _api.post(
      '/auth/signup/register',
      body: {
        'name': draft.name,
        'email': draft.email,
        'password': draft.password,
        'cpf': draft.cpf,
        if (draft.phone != null) 'phone': draft.phone,
        'address': {
          'zip_code': draft.address.zipCode,
          'state': draft.address.state,
          'neighborhood': draft.address.neighborhood,
          'street_name': draft.address.streetName,
          'number': draft.address.number,
          if (draft.address.complement != null)
            'complement': draft.address.complement,
        },
      },
    );
  }

  Future<Map<String, dynamic>> createAddress({
    required String zipCode,
    required String state,
    required String neighborhood,
    required String streetName,
    required String number,
    String? complement,
  }) async {
    return _api.post(
      '/addresses/',
      body: {
        'zip_code': zipCode,
        'state': state,
        'neighborhood': neighborhood,
        'street_name': streetName,
        'number': number,
        if (complement != null) 'complement': complement,
      },
    );
  }

  Future<Map<String, dynamic>> createProperty({
    required int ownerId,
    required int addressId,
    required String name,
    required String propertyType,
    required double sizeHectares,
  }) async {
    return _api.post(
      '/properties/',
      body: {
        'name': name,
        'size': sizeHectares,
        'property_type': propertyType,
        'owner_id': ownerId,
        'address_id': addressId,
      },
    );
  }
}

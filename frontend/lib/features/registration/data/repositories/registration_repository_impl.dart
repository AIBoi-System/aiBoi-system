import 'package:ai_boi/core/network/api_exception.dart';
import 'package:ai_boi/features/registration/data/datasources/registration_remote_data_source.dart';
import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';
import 'package:ai_boi/features/registration/domain/repositories/registration_repository.dart';

class RegistrationRepositoryImpl implements RegistrationRepository {
  RegistrationRepositoryImpl({required RegistrationRemoteDataSource remote})
    : _remote = remote;

  final RegistrationRemoteDataSource _remote;

  static const Map<String, String> _propertyTypeToApi = {
    'Cria': 'REARING',
    'Corte': 'BEEF',
    'Leite': 'DAIRY',
    'Mista': 'MIXED',
    'Recria': 'REARING',
    'Confinamento': 'FEEDLOT',
  };

  @override
  Future<void> sendVerificationCode(String email) async {
    try {
      await _remote.sendVerificationCode(email);
    } on ApiException {
      rethrow;
    } catch (e) {
      throw ApiException('Unable to send verification code.');
    }
  }

  @override
  Future<bool> verifyEmailCode(String email, String code) async {
    await _remote.verifyEmailCode(email, code);
    return true;
  }

  @override
  Future<void> sendPhoneVerificationCode(String phone) async {
    await _remote.sendPhoneVerificationCode(phone);
  }

  @override
  Future<bool> verifyPhoneCode(String phone, String code) async {
    await _remote.verifyPhoneCode(phone, code);
    return true;
  }

  @override
  Future<RegistrationDraft> registerUser(RegistrationDraft draft) async {
    final response = await _remote.registerUser(draft);
    final userId = response['user_id'] as int?;
    final addressId = response['address_id'] as int?;
    final token = response['access_token'] as String?;
    final refreshToken = response['refresh_token'] as String?;
    final role = response['role'] as String?;

    if (userId == null || addressId == null) {
      throw ApiException('Invalid registration response from server.');
    }
    return draft.copyWith(
      userId: userId,
      userAddressId: addressId,
      accessToken: token,
      refreshToken: refreshToken,
      role: role,
    );
  }

  @override
  Future<RegistrationDraft> registerUserWithGoogle(
    RegistrationDraft draft,
    String idToken,
  ) async {
    final response = await _remote.registerUserWithGoogle(draft, idToken);
    final userId = response['user_id'] as int?;
    final addressId = response['address_id'] as int?;
    final token = response['access_token'] as String?;
    final refreshToken = response['refresh_token'] as String?;
    final role = response['role'] as String?;

    if (userId == null || addressId == null) {
      throw ApiException('Invalid registration response from server.');
    }
    return draft.copyWith(
      userId: userId,
      userAddressId: addressId,
      accessToken: token,
      refreshToken: refreshToken,
      role: role,
    );
  }

  @override
  Future<RegisteredProperty> createProperty({
    required int ownerId,
    required int addressId,
    required PropertyDraft property,
  }) async {
    final location = _parseCityState(property.cityState);
    final addressResponse = await _remote.createAddress(
      zipCode: '00000000',
      state: location.state,
      neighborhood: location.city,
      streetName: 'Rural property',
      number: 'S/N',
    );
    final propertyAddressId =
        addressResponse['id_address'] as int? ?? addressId;

    final apiType = _propertyTypeToApi[property.propertyType] ?? 'BEEF';
    final response = await _remote.createProperty(
      ownerId: ownerId,
      addressId: propertyAddressId,
      name: property.name,
      propertyType: apiType,
      sizeHectares: property.sizeHectares,
    );

    return RegisteredProperty(
      id: response['id_property'] as int? ?? 0,
      name: property.name,
      cityState: property.cityState,
      purpose: property.propertyType,
      hectares: property.sizeHectares,
    );
  }

  ({String city, String state}) _parseCityState(String cityState) {
    final parts = cityState.split(RegExp(r'\s*-\s*'));
    if (parts.length >= 2) {
      return (
        city: parts.first.trim(),
        state: parts.last.trim().toUpperCase().substring(0, 2),
      );
    }
    return (city: cityState.trim(), state: 'PA');
  }
}

class AddressDraft {
  final String zipCode;
  final String state;
  final String neighborhood;
  final String streetName;
  final String number;
  final String? complement;

  const AddressDraft({
    required this.zipCode,
    required this.state,
    required this.neighborhood,
    required this.streetName,
    required this.number,
    this.complement,
  });
}

class PropertyDraft {
  final String name;
  final String propertyType;
  final double sizeHectares;
  final String cityState;

  const PropertyDraft({
    required this.name,
    required this.propertyType,
    required this.sizeHectares,
    required this.cityState,
  });
}

class RegistrationDraft {
  final String name;
  final String email;
  final String password;
  final String cpf;
  final String phone;
  final AddressDraft address;
  final int? userId;
  final int? userAddressId;
  final String? accessToken;
  final String? refreshToken;
  final String? role;

  const RegistrationDraft({
    required this.name,
    required this.email,
    required this.password,
    required this.cpf,
    required this.phone,
    required this.address,
    this.userId,
    this.userAddressId,
    this.accessToken,
    this.refreshToken,
    this.role,
  });

  RegistrationDraft copyWith({
    int? userId,
    int? userAddressId,
    String? accessToken,
    String? refreshToken,
    String? role,
  }) {
    return RegistrationDraft(
      name: name,
      email: email,
      password: password,
      cpf: cpf,
      phone: phone,
      address: address,
      userId: userId ?? this.userId,
      userAddressId: userAddressId ?? this.userAddressId,
      accessToken: accessToken ?? this.accessToken,
      refreshToken: refreshToken ?? this.refreshToken,
      role: role ?? this.role,
    );
  }
}

class RegisteredProperty {
  final int id;
  final String name;
  final String cityState;
  final String purpose;
  final double hectares;
  final int? ownerId;
  final int? addressId;

  const RegisteredProperty({
    required this.id,
    required this.name,
    required this.cityState,
    required this.purpose,
    required this.hectares,
    this.ownerId,
    this.addressId,
  });
}

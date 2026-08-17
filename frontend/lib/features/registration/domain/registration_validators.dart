class RegistrationValidators {
  RegistrationValidators._();

  static const Set<String> officialStates = {
    'AC',
    'AL',
    'AP',
    'AM',
    'BA',
    'CE',
    'DF',
    'ES',
    'GO',
    'MA',
    'MT',
    'MS',
    'MG',
    'PA',
    'PB',
    'PR',
    'PE',
    'PI',
    'RJ',
    'RN',
    'RS',
    'RO',
    'RR',
    'SC',
    'SP',
    'SE',
    'TO',
  };

  static const Set<String> officialAreaCodes = {
    '11',
    '12',
    '13',
    '14',
    '15',
    '16',
    '17',
    '18',
    '19',
    '21',
    '22',
    '24',
    '27',
    '28',
    '31',
    '32',
    '33',
    '34',
    '35',
    '37',
    '38',
    '41',
    '42',
    '43',
    '44',
    '45',
    '46',
    '47',
    '48',
    '49',
    '51',
    '53',
    '54',
    '55',
    '61',
    '62',
    '63',
    '64',
    '65',
    '66',
    '67',
    '68',
    '69',
    '71',
    '73',
    '74',
    '75',
    '77',
    '79',
    '81',
    '82',
    '83',
    '84',
    '85',
    '86',
    '87',
    '88',
    '89',
    '91',
    '92',
    '93',
    '94',
    '95',
    '96',
    '97',
    '98',
    '99',
  };

  static String digitsOnly(String value) => value.replaceAll(RegExp(r'\D'), '');

  static String? email(String? value) {
    final normalized = value?.trim() ?? '';
    final pattern = RegExp(r'^[^\s@]+@[^\s@]+\.[^\s@]+$');
    return pattern.hasMatch(normalized) ? null : 'Informe um e-mail válido';
  }

  static String? phone(String? value) {
    final digits = digitsOnly(value ?? '');
    if (digits.length != 10 && digits.length != 11) {
      return 'Telefone deve ter 10 ou 11 dígitos';
    }
    if (!officialAreaCodes.contains(digits.substring(0, 2))) {
      return 'DDD inválido';
    }
    return null;
  }

  static String? cpf(String? value) {
    final digits = digitsOnly(value ?? '');
    if (digits.length != 11 || RegExp(r'^(\d)\1{10}$').hasMatch(digits)) {
      return 'CPF inválido';
    }
    int checkDigit(int length) {
      var sum = 0;
      for (var index = 0; index < length; index++) {
        sum += int.parse(digits[index]) * (length + 1 - index);
      }
      final remainder = sum % 11;
      return remainder < 2 ? 0 : 11 - remainder;
    }

    final first = checkDigit(9);
    final second = checkDigit(10);
    return digits.endsWith('$first$second') ? null : 'CPF inválido';
  }

  static String? zipCode(String? value) {
    return digitsOnly(value ?? '').length == 8
        ? null
        : 'CEP deve ter 8 dígitos';
  }

  static String? state(String? value) {
    final normalized = value?.trim().toUpperCase() ?? '';
    return officialStates.contains(normalized) ? null : 'UF inválida';
  }

  static String? requiredText(String? value, String label) {
    return value == null || value.trim().isEmpty ? 'Informe $label' : null;
  }
}

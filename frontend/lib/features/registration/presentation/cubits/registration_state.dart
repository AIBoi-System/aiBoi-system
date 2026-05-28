import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';

abstract class RegistrationState {}

class RegistrationInitial extends RegistrationState {}

class RegistrationLoading extends RegistrationState {}

class RegistrationError extends RegistrationState {
  final String message;
  RegistrationError(this.message);
}

class RegistrationCodeSent extends RegistrationState {}

class RegistrationEmailVerified extends RegistrationState {}

class RegistrationUserCreated extends RegistrationState {
  final RegistrationDraft draft;
  RegistrationUserCreated(this.draft);
}

class RegistrationPropertyCreated extends RegistrationState {
  final RegisteredProperty property;
  RegistrationPropertyCreated(this.property);
}

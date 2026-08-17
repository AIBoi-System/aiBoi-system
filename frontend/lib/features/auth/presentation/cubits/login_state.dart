abstract class LoginState {}

class LoginInitial extends LoginState {}

class LoginLoading extends LoginState {}

class LoginSuccess extends LoginState {}

class LoginError extends LoginState {
  final String message;
  LoginError(this.message);
}

class GoogleLoginNeedsRegistration extends LoginState {
  final String email;
  final String? name;
  final String idToken;

  GoogleLoginNeedsRegistration({
    required this.email,
    required this.idToken,
    this.name,
  });
}

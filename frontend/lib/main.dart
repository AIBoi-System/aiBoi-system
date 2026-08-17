import 'package:ai_boi/app/app.dart';
import 'package:flutter/material.dart';
import 'package:google_sign_in/google_sign_in.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  const googleClientId = String.fromEnvironment('GOOGLE_CLIENT_ID');
  if (googleClientId.isNotEmpty) {
    await GoogleSignIn.instance.initialize(clientId: googleClientId);
  }
  runApp(const AiBoiApp());
}

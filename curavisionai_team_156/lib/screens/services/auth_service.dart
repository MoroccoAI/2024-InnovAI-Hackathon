import 'package:firebase_auth/firebase_auth.dart';

class AuthService {
  static final FirebaseAuth _auth = FirebaseAuth.instance;

  /// Login user with Firebase Authentication
  static Future<void> login(String email, String password) async {
    try {
      await _auth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );
    } on FirebaseAuthException catch (e) {
      // Log the error code for debugging
      print("FirebaseAuthException Code: ${e.code}");
      print("FirebaseAuthException Message: ${e.message}");

      if (e.code == 'user-not-found') {
        throw Exception('No user found with this email address.');
      } else if (e.code == 'wrong-password') {
        throw Exception('The password entered is incorrect.');
      } else if (e.code == 'invalid-email') {
        throw Exception('The email address entered is invalid.');
      } else if (e.code == 'user-disabled') {
        throw Exception('This user account has been disabled. Please contact support.');
      } else {
        // Log unhandled FirebaseAuth errors
        throw Exception('Login failed due to an unknown error. Please try again.');
      }
    } catch (e) {
      // Log unknown errors
      print("Unknown error during login: $e");
      throw Exception('An unknown error occurred during login. Please try again later.');
    }
  }

  /// Sign up user with Firebase Authentication
  static Future<bool> signup(String name, String email, String password) async {
    try {
      UserCredential userCredential = await _auth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );

      // Update the user's display name
      await userCredential.user?.updateDisplayName(name);
      await userCredential.user?.reload();

      return true; // Sign up successful
    } on FirebaseAuthException catch (e) {
      if (e.code == 'email-already-in-use') {
        throw Exception('The email address is already in use by another account.');
      } else if (e.code == 'invalid-email') {
        throw Exception('The email address entered is invalid.');
      } else if (e.code == 'weak-password') {
        throw Exception('The password provided is too weak.');
      } else {
        print("Unhandled FirebaseAuthException: ${e.code}");
        throw Exception('Sign up failed due to an unknown error. Please try again.');
      }
    } catch (e) {
      print("Unknown error during sign up: $e");
      throw Exception('An unknown error occurred during sign up. Please try again later.');
    }
  }

  /// Reset password using Firebase Authentication
  static Future<bool> resetPassword(String email) async {
    try {
      await _auth.sendPasswordResetEmail(email: email);
      return true; // Reset link sent successfully
    } on FirebaseAuthException catch (e) {
      if (e.code == 'invalid-email') {
        throw Exception('The email address entered is invalid.');
      } else if (e.code == 'user-not-found') {
        throw Exception('No user found with this email address.');
      } else {
        print("Unhandled FirebaseAuthException: ${e.code}");
        throw Exception('Failed to send password reset link. Please try again.');
      }
    } catch (e) {
      print("Unknown error during password reset: $e");
      throw Exception('An unknown error occurred during password reset. Please try again later.');
    }
  }

  /// Sign out user
  static Future<void> signOut() async {
    await _auth.signOut();
  }
}
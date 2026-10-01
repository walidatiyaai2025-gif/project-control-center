import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import 'repository_home.dart';
import 'token_page.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const RepoLiveApp());
}

class RepoLiveApp extends StatelessWidget {
  const RepoLiveApp({super.key});

  @override
  Widget build(BuildContext context) {
    final scheme = ColorScheme.fromSeed(
      seedColor: const Color(0xFF0969DA),
      brightness: Brightness.light,
    );
    return MaterialApp(
      title: 'PCC Repo Live',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: scheme,
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFFF6F8FA),
        cardTheme: const CardThemeData(
          elevation: 0,
          margin: EdgeInsets.zero,
        ),
        inputDecorationTheme: const InputDecorationTheme(
          border: OutlineInputBorder(),
          isDense: true,
        ),
      ),
      home: const AuthGate(),
    );
  }
}

class AuthGate extends StatefulWidget {
  const AuthGate({super.key});

  @override
  State<AuthGate> createState() => _AuthGateState();
}

class _AuthGateState extends State<AuthGate> {
  static const _storage = FlutterSecureStorage();
  String? _token;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _restore();
  }

  Future<void> _restore() async {
    final token = await _storage.read(key: 'github_token');
    if (!mounted) return;
    setState(() {
      _token = token;
      _loading = false;
    });
  }

  Future<void> _signOut() async {
    await _storage.delete(key: 'github_token');
    await _storage.delete(key: 'selected_repo');
    if (!mounted) return;
    setState(() => _token = null);
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }
    if (_token == null || _token!.isEmpty) {
      return TokenPage(
        onAuthenticated: (token) {
          setState(() => _token = token);
        },
      );
    }
    return RepositoryHome(
      token: _token!,
      onSignOut: _signOut,
    );
  }
}

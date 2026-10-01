import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import 'branch_dashboard.dart';
import 'github_api.dart';
import 'models.dart';

class RepositoryHome extends StatefulWidget {
  const RepositoryHome({
    super.key,
    required this.token,
    required this.onSignOut,
  });

  final String token;
  final Future<void> Function() onSignOut;

  @override
  State<RepositoryHome> createState() => _RepositoryHomeState();
}

class _RepositoryHomeState extends State<RepositoryHome> {
  static const _storage = FlutterSecureStorage();
  late final GitHubApi _api;
  List<RepoInfo> _repos = const [];
  RepoInfo? _selected;
  String _login = '';
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _api = GitHubApi(widget.token);
    _load();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final values = await Future.wait<dynamic>([
        _api.getUser(),
        _api.getRepositories(),
      ]);
      final user = (values[0] as Map).cast<String, dynamic>();
      final repos = values[1] as List<RepoInfo>;
      final remembered = await _storage.read(key: 'selected_repo');
      RepoInfo? chosen;
      if (remembered != null) {
        for (final repo in repos) {
          if (repo.fullName == remembered) {
            chosen = repo;
            break;
          }
        }
      }
      chosen ??= repos.isEmpty ? null : repos.first;
      if (!mounted) return;
      setState(() {
        _login = user['login']?.toString() ?? '';
        _repos = repos;
        _selected = chosen;
        _loading = false;
      });
    } on GitHubApiException catch (e) {
      if (!mounted) return;
      setState(() {
        _error = e.message;
        _loading = false;
      });
    } catch (_) {
      if (!mounted) return;
      setState(() {
        _error = 'Unable to load repositories.';
        _loading = false;
      });
    }
  }

  Future<void> _select(RepoInfo? value) async {
    if (value == null) return;
    setState(() => _selected = value);
    await _storage.write(key: 'selected_repo', value: value.fullName);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('PCC Repo Live'),
        backgroundColor: Colors.white,
        surfaceTintColor: Colors.white,
        actions: [
          if (_login.isNotEmpty)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 6),
              child: Center(
                child: Text(
                  '@' + _login,
                  style: const TextStyle(fontWeight: FontWeight.w600),
                ),
              ),
            ),
          IconButton(
            tooltip: 'Reload repositories',
            onPressed: _loading ? null : _load,
            icon: const Icon(Icons.refresh),
          ),
          PopupMenuButton<String>(
            onSelected: (value) {
              if (value == 'signout') widget.onSignOut();
            },
            itemBuilder: (_) => const [
              PopupMenuItem(
                value: 'signout',
                child: Row(
                  children: [
                    Icon(Icons.logout),
                    SizedBox(width: 8),
                    Text('Disconnect GitHub'),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? _ErrorState(message: _error!, onRetry: _load)
              : _repos.isEmpty
                  ? const Center(child: Text('No repositories are visible to this token.'))
                  : Column(
                      children: [
                        Container(
                          color: Colors.white,
                          padding: const EdgeInsets.fromLTRB(16, 14, 16, 14),
                          child: DropdownButtonFormField<RepoInfo>(
                            key: ValueKey(_selected?.fullName),
                            initialValue: _selected,
                            isExpanded: true,
                            decoration: const InputDecoration(
                              labelText: 'Project / repository',
                              prefixIcon: Icon(Icons.folder_open),
                            ),
                            items: _repos
                                .map(
                                  (repo) => DropdownMenuItem(
                                    value: repo,
                                    child: Row(
                                      children: [
                                        Icon(
                                          repo.isPrivate ? Icons.lock_outline : Icons.public,
                                          size: 18,
                                        ),
                                        const SizedBox(width: 8),
                                        Expanded(
                                          child: Text(
                                            repo.fullName,
                                            overflow: TextOverflow.ellipsis,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                )
                                .toList(),
                            onChanged: _select,
                          ),
                        ),
                        Expanded(
                          child: _selected == null
                              ? const SizedBox.shrink()
                              : BranchDashboard(
                                  key: ValueKey(_selected!.fullName),
                                  api: _api,
                                  repo: _selected!,
                                  currentLogin: _login,
                                ),
                        ),
                      ],
                    ),
    );
  }
}

class _ErrorState extends StatelessWidget {
  const _ErrorState({required this.message, required this.onRetry});

  final String message;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.cloud_off, size: 48, color: Theme.of(context).colorScheme.error),
            const SizedBox(height: 12),
            Text(message, textAlign: TextAlign.center),
            const SizedBox(height: 16),
            FilledButton.icon(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh),
              label: const Text('Retry'),
            ),
          ],
        ),
      ),
    );
  }
}

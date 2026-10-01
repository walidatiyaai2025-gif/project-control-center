import 'dart:async';

import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import 'github_api.dart';
import 'models.dart';

enum BranchTab { overview, yours, active, stale, all }

class BranchDashboard extends StatefulWidget {
  const BranchDashboard({
    super.key,
    required this.api,
    required this.repo,
    required this.currentLogin,
  });

  final GitHubApi api;
  final RepoInfo repo;
  final String currentLogin;

  @override
  State<BranchDashboard> createState() => _BranchDashboardState();
}

class _BranchDashboardState extends State<BranchDashboard> {
  final _searchController = TextEditingController();
  final Map<String, BranchSummary> _cache = {};
  Timer? _timer;
  List<BranchSummary> _branches = const [];
  BranchTab _tab = BranchTab.overview;
  bool _loading = true;
  bool _refreshing = false;
  String? _error;
  int _refreshCycle = 0;
  DateTime? _lastUpdated;

  @override
  void initState() {
    super.initState();
    _load(forceAll: true);
    _timer = Timer.periodic(const Duration(seconds: 15), (_) {
      _load(silent: true);
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _load({bool silent = false, bool forceAll = false}) async {
    if (_refreshing) return;
    _refreshing = true;
    if (!silent && _branches.isEmpty && mounted) {
      setState(() {
        _loading = true;
        _error = null;
      });
    }

    try {
      final raw = await widget.api.getBranches(widget.repo.fullName);
      _refreshCycle++;
      final periodicFullRefresh = _refreshCycle % 4 == 0;
      final summaries = <BranchSummary>[];

      for (var i = 0; i < raw.length; i += 4) {
        final end = (i + 4) > raw.length ? raw.length : i + 4;
        final slice = raw.sublist(i, end);
        final futures = slice.map((branch) async {
          final name = branch['name']?.toString() ?? '';
          final commit = (branch['commit'] as Map?)?.cast<String, dynamic>() ?? const {};
          final sha = commit['sha']?.toString() ?? '';
          final old = _cache[name];
          final shouldRefresh = forceAll ||
              periodicFullRefresh ||
              old == null ||
              old.sha != sha ||
              old.isPending;

          if (!shouldRefresh && old != null) return old;

          final value = await widget.api.getBranchSummary(
            repo: widget.repo,
            rawBranch: branch,
            currentLogin: widget.currentLogin,
          );
          _cache[name] = value;
          return value;
        });
        summaries.addAll(await Future.wait(futures));
      }

      final liveNames = raw.map((e) => e['name']?.toString() ?? '').toSet();
      _cache.removeWhere((key, _) => !liveNames.contains(key));

      summaries.sort((a, b) {
        if (a.name == widget.repo.defaultBranch) return -1;
        if (b.name == widget.repo.defaultBranch) return 1;
        final ad = a.updatedAt ?? DateTime.fromMillisecondsSinceEpoch(0);
        final bd = b.updatedAt ?? DateTime.fromMillisecondsSinceEpoch(0);
        return bd.compareTo(ad);
      });

      if (!mounted) return;
      setState(() {
        _branches = summaries;
        _lastUpdated = DateTime.now();
        _loading = false;
        _error = null;
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
        _error = 'Unable to refresh branch data.';
        _loading = false;
      });
    } finally {
      _refreshing = false;
    }
  }

  List<BranchSummary> get _filtered {
    final now = DateTime.now();
    final staleCutoff = now.subtract(const Duration(days: 90));
    Iterable<BranchSummary> values = _branches;

    switch (_tab) {
      case BranchTab.overview:
        values = values.where((b) => b.name == widget.repo.defaultBranch);
      case BranchTab.yours:
        values = values.where((b) => b.isMine);
      case BranchTab.active:
        values = values.where(
          (b) =>
              b.name != widget.repo.defaultBranch &&
              (b.updatedAt == null || b.updatedAt!.isAfter(staleCutoff)),
        );
      case BranchTab.stale:
        values = values.where(
          (b) =>
              b.name != widget.repo.defaultBranch &&
              b.updatedAt != null &&
              b.updatedAt!.isBefore(staleCutoff),
        );
      case BranchTab.all:
        break;
    }

    final query = _searchController.text.trim().toLowerCase();
    if (query.isNotEmpty) {
      values = values.where((b) => b.name.toLowerCase().contains(query));
    }
    return values.toList();
  }

  int _count(BranchTab tab) {
    final before = _tab;
    _tab = tab;
    final value = _filtered.length;
    _tab = before;
    return value;
  }

  String _tabLabel(BranchTab tab) {
    switch (tab) {
      case BranchTab.overview:
        return 'Default';
      case BranchTab.yours:
        return 'Yours';
      case BranchTab.active:
        return 'Active';
      case BranchTab.stale:
        return 'Stale';
      case BranchTab.all:
        return 'All';
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_error != null && _branches.isEmpty) {
      return _FullError(
        message: _error!,
        onRetry: () => _load(forceAll: true),
      );
    }

    final items = _filtered;

    return RefreshIndicator(
      onRefresh: () => _load(forceAll: true),
      child: ListView(
        physics: const AlwaysScrollableScrollPhysics(),
        padding: const EdgeInsets.all(16),
        children: [
          _RepoHeader(
            repo: widget.repo,
            branchCount: _branches.length,
            lastUpdated: _lastUpdated,
            refreshing: _refreshing,
            onRefresh: () => _load(forceAll: true),
          ),
          const SizedBox(height: 14),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: BranchTab.values.map((tab) {
                return Padding(
                  padding: const EdgeInsets.only(right: 8),
                  child: ChoiceChip(
                    selected: _tab == tab,
                    label: Text(_tabLabel(tab) + '  ' + _count(tab).toString()),
                    onSelected: (_) => setState(() => _tab = tab),
                  ),
                );
              }).toList(),
            ),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _searchController,
            onChanged: (_) => setState(() {}),
            decoration: InputDecoration(
              hintText: 'Search branches…',
              prefixIcon: const Icon(Icons.search),
              suffixIcon: _searchController.text.isEmpty
                  ? null
                  : IconButton(
                      onPressed: () {
                        _searchController.clear();
                        setState(() {});
                      },
                      icon: const Icon(Icons.close),
                    ),
            ),
          ),
          if (_error != null) ...[
            const SizedBox(height: 10),
            MaterialBanner(
              content: Text(_error!),
              actions: [
                TextButton(
                  onPressed: () => _load(forceAll: true),
                  child: const Text('Retry'),
                ),
              ],
            ),
          ],
          const SizedBox(height: 12),
          if (items.isEmpty)
            const _EmptyBranches()
          else
            ...items.map(
              (branch) => Padding(
                padding: const EdgeInsets.only(bottom: 10),
                child: _BranchCard(
                  repo: widget.repo,
                  branch: branch,
                ),
              ),
            ),
          const SizedBox(height: 40),
        ],
      ),
    );
  }
}

class _RepoHeader extends StatelessWidget {
  const _RepoHeader({
    required this.repo,
    required this.branchCount,
    required this.lastUpdated,
    required this.refreshing,
    required this.onRefresh,
  });

  final RepoInfo repo;
  final int branchCount;
  final DateTime? lastUpdated;
  final bool refreshing;
  final VoidCallback onRefresh;

  @override
  Widget build(BuildContext context) {
    return Card(
      shape: RoundedRectangleBorder(
        side: BorderSide(color: Theme.of(context).dividerColor),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Padding(
        padding: const EdgeInsets.fromLTRB(16, 14, 12, 14),
        child: Row(
          children: [
            CircleAvatar(
              child: Icon(repo.isPrivate ? Icons.lock_outline : Icons.account_tree_outlined),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    repo.fullName,
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.w700,
                        ),
                  ),
                  const SizedBox(height: 3),
                  Text(
                    branchCount.toString() +
                        ' branches · Live refresh every 15s' +
                        (lastUpdated == null ? '' : ' · ' + _relative(lastUpdated!)),
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                ],
              ),
            ),
            IconButton(
              tooltip: 'Refresh now',
              onPressed: refreshing ? null : onRefresh,
              icon: refreshing
                  ? const SizedBox.square(
                      dimension: 18,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Icon(Icons.refresh),
            ),
          ],
        ),
      ),
    );
  }
}

class _BranchCard extends StatelessWidget {
  const _BranchCard({required this.repo, required this.branch});

  final RepoInfo repo;
  final BranchSummary branch;

  Future<void> _open(String value) async {
    final uri = Uri.tryParse(value);
    if (uri != null) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDefault = branch.name == repo.defaultBranch;
    final status = _CheckStatus.from(branch);

    return Card(
      clipBehavior: Clip.antiAlias,
      shape: RoundedRectangleBorder(
        side: BorderSide(color: Theme.of(context).dividerColor),
        borderRadius: BorderRadius.circular(10),
      ),
      child: InkWell(
        onTap: () => _open(branch.branchUrl(repo)),
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Icon(Icons.account_tree, size: 20),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      branch.name,
                      style: const TextStyle(fontWeight: FontWeight.w700),
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  if (isDefault)
                    const Padding(
                      padding: EdgeInsets.only(left: 8),
                      child: Chip(
                        visualDensity: VisualDensity.compact,
                        label: Text('Default'),
                      ),
                    ),
                ],
              ),
              const SizedBox(height: 10),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                crossAxisAlignment: WrapCrossAlignment.center,
                children: [
                  _StatusPill(status: status),
                  _InfoPill(
                    icon: Icons.schedule,
                    text: branch.updatedAt == null ? 'Updated —' : _relative(branch.updatedAt!),
                  ),
                  _InfoPill(
                    icon: Icons.arrow_downward,
                    text: 'Behind ' + branch.behind.toString(),
                  ),
                  _InfoPill(
                    icon: Icons.arrow_upward,
                    text: 'Ahead ' + branch.ahead.toString(),
                  ),
                  if (branch.isMine)
                    const _InfoPill(
                      icon: Icons.person_outline,
                      text: 'Yours',
                    ),
                  if (branch.pullRequestNumber != null)
                    ActionChip(
                      avatar: const Icon(Icons.call_merge, size: 16),
                      label: Text('PR #' + branch.pullRequestNumber.toString()),
                      onPressed: branch.pullRequestUrl == null
                          ? null
                          : () => _open(branch.pullRequestUrl!),
                    ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _CheckStatus {
  const _CheckStatus({
    required this.label,
    required this.icon,
    required this.kind,
  });

  final String label;
  final IconData icon;
  final int kind;

  factory _CheckStatus.from(BranchSummary branch) {
    if (!branch.hasChecks) {
      return const _CheckStatus(
        label: 'No checks',
        icon: Icons.remove_circle_outline,
        kind: 0,
      );
    }
    final count = branch.checksCompleted.toString() + ' / ' + branch.checksTotal.toString();
    if (branch.hasFailures) {
      return _CheckStatus(
        label: count + ' · failed',
        icon: Icons.cancel,
        kind: 2,
      );
    }
    if (branch.isPending) {
      return _CheckStatus(
        label: count + ' · running',
        icon: Icons.pending,
        kind: 1,
      );
    }
    return _CheckStatus(
      label: count,
      icon: Icons.check_circle,
      kind: 3,
    );
  }
}

class _StatusPill extends StatelessWidget {
  const _StatusPill({required this.status});

  final _CheckStatus status;

  @override
  Widget build(BuildContext context) {
    Color foreground;
    Color background;
    switch (status.kind) {
      case 1:
        foreground = const Color(0xFF9A6700);
        background = const Color(0xFFFFF8C5);
      case 2:
        foreground = const Color(0xFFCF222E);
        background = const Color(0xFFFFEBE9);
      case 3:
        foreground = const Color(0xFF1A7F37);
        background = const Color(0xFFDAFBE1);
      default:
        foreground = const Color(0xFF57606A);
        background = const Color(0xFFF6F8FA);
    }
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 6),
      decoration: BoxDecoration(
        color: background,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(status.icon, size: 16, color: foreground),
          const SizedBox(width: 5),
          Text(
            status.label,
            style: TextStyle(
              color: foreground,
              fontWeight: FontWeight.w700,
              fontSize: 12,
            ),
          ),
        ],
      ),
    );
  }
}

class _InfoPill extends StatelessWidget {
  const _InfoPill({required this.icon, required this.text});

  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 6),
      decoration: BoxDecoration(
        border: Border.all(color: Theme.of(context).dividerColor),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 15),
          const SizedBox(width: 5),
          Text(text, style: const TextStyle(fontSize: 12)),
        ],
      ),
    );
  }
}

class _EmptyBranches extends StatelessWidget {
  const _EmptyBranches();

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 48),
      child: Column(
        children: [
          Icon(Icons.filter_alt_off, size: 42, color: Theme.of(context).colorScheme.outline),
          const SizedBox(height: 10),
          const Text('No branches match this filter.'),
        ],
      ),
    );
  }
}

class _FullError extends StatelessWidget {
  const _FullError({required this.message, required this.onRetry});

  final String message;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) {
    return ListView(
      physics: const AlwaysScrollableScrollPhysics(),
      padding: const EdgeInsets.all(24),
      children: [
        const SizedBox(height: 80),
        Icon(Icons.error_outline, size: 52, color: Theme.of(context).colorScheme.error),
        const SizedBox(height: 12),
        Text(message, textAlign: TextAlign.center),
        const SizedBox(height: 16),
        Center(
          child: FilledButton.icon(
            onPressed: onRetry,
            icon: const Icon(Icons.refresh),
            label: const Text('Retry'),
          ),
        ),
      ],
    );
  }
}

String _relative(DateTime value) {
  final diff = DateTime.now().difference(value);
  if (diff.inSeconds < 20) return 'just now';
  if (diff.inMinutes < 1) return diff.inSeconds.toString() + 's ago';
  if (diff.inHours < 1) return diff.inMinutes.toString() + 'm ago';
  if (diff.inDays < 1) return diff.inHours.toString() + 'h ago';
  if (diff.inDays < 30) return diff.inDays.toString() + 'd ago';
  final months = (diff.inDays / 30).floor();
  if (months < 12) return months.toString() + 'mo ago';
  return (months / 12).floor().toString() + 'y ago';
}

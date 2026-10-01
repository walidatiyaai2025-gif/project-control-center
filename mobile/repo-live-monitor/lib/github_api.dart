import 'dart:async';
import 'dart:convert';

import 'package:http/http.dart' as http;

import 'models.dart';

class GitHubApiException implements Exception {
  GitHubApiException(this.message, {this.statusCode, this.rateLimitReset});

  final String message;
  final int? statusCode;
  final DateTime? rateLimitReset;

  @override
  String toString() => message;
}

class GitHubApi {
  GitHubApi(this.token);

  final String token;
  static const String _host = 'api.github.com';

  Map<String, String> get _headers => {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + token,
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'PCC-Repo-Live',
      };

  Uri _uri(String path, [Map<String, String>? query]) {
    return Uri.https(_host, path, query);
  }

  Future<dynamic> _get(Uri uri) async {
    late http.Response response;
    try {
      response = await http.get(uri, headers: _headers).timeout(const Duration(seconds: 25));
    } on TimeoutException {
      throw GitHubApiException('GitHub request timed out. Pull to refresh and try again.');
    } catch (e) {
      throw GitHubApiException('Network error while contacting GitHub.');
    }

    if (response.statusCode >= 200 && response.statusCode < 300) {
      if (response.body.isEmpty) return const {};
      return jsonDecode(response.body);
    }

    DateTime? reset;
    final resetHeader = response.headers['x-ratelimit-reset'];
    if (resetHeader != null) {
      final epoch = int.tryParse(resetHeader);
      if (epoch != null) {
        reset = DateTime.fromMillisecondsSinceEpoch(epoch * 1000, isUtc: true).toLocal();
      }
    }

    String message = 'GitHub request failed (' + response.statusCode.toString() + ').';
    try {
      final body = jsonDecode(response.body);
      if (body is Map && body['message'] != null) {
        message = body['message'].toString();
      }
    } catch (_) {}

    if (response.statusCode == 401) {
      message = 'GitHub token is invalid or expired.';
    } else if (response.statusCode == 403 && response.headers['x-ratelimit-remaining'] == '0') {
      message = reset == null
          ? 'GitHub API rate limit reached.'
          : 'GitHub API rate limit reached. Resets at ' + reset.toString();
    }

    throw GitHubApiException(
      message,
      statusCode: response.statusCode,
      rateLimitReset: reset,
    );
  }

  Future<dynamic> _safeGet(Uri uri, dynamic fallback) async {
    try {
      return await _get(uri);
    } on GitHubApiException catch (e) {
      if (e.statusCode == 401) rethrow;
      return fallback;
    }
  }

  Future<Map<String, dynamic>> getUser() async {
    final data = await _get(_uri('/user'));
    return (data as Map).cast<String, dynamic>();
  }

  Future<List<RepoInfo>> getRepositories() async {
    final output = <RepoInfo>[];
    for (var page = 1; page <= 20; page++) {
      final data = await _get(_uri('/user/repos', {
        'affiliation': 'owner,collaborator,organization_member',
        'visibility': 'all',
        'sort': 'updated',
        'direction': 'desc',
        'per_page': '100',
        'page': page.toString(),
      }));
      final list = (data as List).cast<dynamic>();
      output.addAll(list.map((e) => RepoInfo.fromJson((e as Map).cast<String, dynamic>())));
      if (list.length < 100) break;
    }
    return output;
  }

  Future<List<Map<String, dynamic>>> getBranches(String fullName) async {
    final output = <Map<String, dynamic>>[];
    for (var page = 1; page <= 20; page++) {
      final data = await _get(_uri('/repos/' + fullName + '/branches', {
        'per_page': '100',
        'page': page.toString(),
      }));
      final list = (data as List).cast<dynamic>();
      output.addAll(list.map((e) => (e as Map).cast<String, dynamic>()));
      if (list.length < 100) break;
    }
    return output;
  }

  Future<BranchSummary> getBranchSummary({
    required RepoInfo repo,
    required Map<String, dynamic> rawBranch,
    required String currentLogin,
  }) async {
    final name = rawBranch['name']?.toString() ?? '';
    final commitMap = (rawBranch['commit'] as Map?)?.cast<String, dynamic>() ?? const {};
    final sha = commitMap['sha']?.toString() ?? '';

    final encodedSha = Uri.encodeComponent(sha);
    final encodedBase = Uri.encodeComponent(repo.defaultBranch);
    final encodedHead = Uri.encodeComponent(name);

    final results = await Future.wait<dynamic>([
      _safeGet(_uri('/repos/' + repo.fullName + '/commits/' + encodedSha), const {}),
      _safeGet(_uri('/repos/' + repo.fullName + '/compare/' + encodedBase + '...' + encodedHead), const {}),
      _safeGet(_uri('/repos/' + repo.fullName + '/commits/' + encodedSha + '/check-runs', {
        'per_page': '100',
      }), const {'check_runs': []}),
      _safeGet(_uri('/repos/' + repo.fullName + '/commits/' + encodedSha + '/status'), const {'statuses': []}),
      _safeGet(_uri('/repos/' + repo.fullName + '/pulls', {
        'state': 'open',
        'head': repo.owner + ':' + name,
        'per_page': '1',
      }), const []),
    ]);

    final commit = results[0] is Map ? (results[0] as Map).cast<String, dynamic>() : <String, dynamic>{};
    final compare = results[1] is Map ? (results[1] as Map).cast<String, dynamic>() : <String, dynamic>{};
    final checks = results[2] is Map ? (results[2] as Map).cast<String, dynamic>() : <String, dynamic>{};
    final statuses = results[3] is Map ? (results[3] as Map).cast<String, dynamic>() : <String, dynamic>{};
    final pulls = results[4] is List ? (results[4] as List).cast<dynamic>() : <dynamic>[];

    final commitDetail = (commit['commit'] as Map?)?.cast<String, dynamic>() ?? const {};
    final committerDetail = (commitDetail['committer'] as Map?)?.cast<String, dynamic>() ?? const {};
    final authorDetail = (commitDetail['author'] as Map?)?.cast<String, dynamic>() ?? const {};
    final dateText = committerDetail['date']?.toString() ?? authorDetail['date']?.toString();
    final updatedAt = dateText == null ? null : DateTime.tryParse(dateText)?.toLocal();

    final author = (commit['author'] as Map?)?.cast<String, dynamic>() ?? const {};
    final committer = (commit['committer'] as Map?)?.cast<String, dynamic>() ?? const {};
    final isMine = author['login']?.toString().toLowerCase() == currentLogin.toLowerCase() ||
        committer['login']?.toString().toLowerCase() == currentLogin.toLowerCase();

    final checkRuns = (checks['check_runs'] as List?)?.cast<dynamic>() ?? const [];
    final statusList = (statuses['statuses'] as List?)?.cast<dynamic>() ?? const [];

    var completed = 0;
    var failed = 0;
    var pending = 0;

    const badConclusions = {
      'failure',
      'timed_out',
      'cancelled',
      'action_required',
      'startup_failure',
      'stale',
    };

    for (final item in checkRuns) {
      final row = (item as Map).cast<String, dynamic>();
      final status = row['status']?.toString();
      final conclusion = row['conclusion']?.toString();
      if (status == 'completed') {
        completed++;
        if (conclusion != null && badConclusions.contains(conclusion)) failed++;
      } else {
        pending++;
      }
    }

    for (final item in statusList) {
      final row = (item as Map).cast<String, dynamic>();
      final state = row['state']?.toString();
      if (state == 'pending') {
        pending++;
      } else {
        completed++;
        if (state == 'failure' || state == 'error') failed++;
      }
    }

    int? prNumber;
    String? prUrl;
    if (pulls.isNotEmpty) {
      final pr = (pulls.first as Map).cast<String, dynamic>();
      prNumber = pr['number'] is int ? pr['number'] as int : int.tryParse(pr['number']?.toString() ?? '');
      prUrl = pr['html_url']?.toString();
    }

    return BranchSummary(
      name: name,
      sha: sha,
      updatedAt: updatedAt,
      isMine: isMine,
      ahead: _asInt(compare['ahead_by']),
      behind: _asInt(compare['behind_by']),
      checksTotal: checkRuns.length + statusList.length,
      checksCompleted: completed,
      checksFailed: failed,
      checksPending: pending,
      pullRequestNumber: prNumber,
      pullRequestUrl: prUrl,
    );
  }

  int _asInt(dynamic value) {
    if (value is int) return value;
    return int.tryParse(value?.toString() ?? '') ?? 0;
  }
}

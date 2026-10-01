class RepoInfo {
  const RepoInfo({
    required this.name,
    required this.fullName,
    required this.owner,
    required this.defaultBranch,
    required this.isPrivate,
  });

  final String name;
  final String fullName;
  final String owner;
  final String defaultBranch;
  final bool isPrivate;

  factory RepoInfo.fromJson(Map<String, dynamic> json) {
    final ownerJson = (json['owner'] as Map?)?.cast<String, dynamic>() ?? const {};
    return RepoInfo(
      name: json['name']?.toString() ?? '',
      fullName: json['full_name']?.toString() ?? '',
      owner: ownerJson['login']?.toString() ?? '',
      defaultBranch: json['default_branch']?.toString() ?? 'main',
      isPrivate: json['private'] == true,
    );
  }

  @override
  String toString() => fullName;
}

class BranchSummary {
  const BranchSummary({
    required this.name,
    required this.sha,
    required this.updatedAt,
    required this.isMine,
    required this.ahead,
    required this.behind,
    required this.checksTotal,
    required this.checksCompleted,
    required this.checksFailed,
    required this.checksPending,
    required this.pullRequestNumber,
    required this.pullRequestUrl,
  });

  final String name;
  final String sha;
  final DateTime? updatedAt;
  final bool isMine;
  final int ahead;
  final int behind;
  final int checksTotal;
  final int checksCompleted;
  final int checksFailed;
  final int checksPending;
  final int? pullRequestNumber;
  final String? pullRequestUrl;

  bool get hasChecks => checksTotal > 0;
  bool get hasFailures => checksFailed > 0;
  bool get isPending => checksPending > 0;

  String branchUrl(RepoInfo repo) {
    return 'https://github.com/' + repo.fullName + '/tree/' + Uri.encodeFull(name);
  }
}

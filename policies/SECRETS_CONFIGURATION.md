# Secrets and Configuration

Secrets must never be committed to source, prompts, status files, logs, examples, screenshots, or artifacts. Repositories should use platform secret stores and least-privilege credentials.

Configuration must distinguish environment-specific values from source-controlled defaults. Required configuration keys may be documented, but secret values must not be. Rotation/revocation is mandatory after suspected exposure.

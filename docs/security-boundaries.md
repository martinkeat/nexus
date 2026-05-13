# Nexus Security Boundaries

## Authentication

- Nexus requires a single admin account created during first-run setup.
- No anonymous access is permitted by default.
- Sessions are managed via secure HTTP-only cookies with configurable timeout.
- API access is available via bearer tokens managed in the Nexus settings UI.

## Internal Service Isolation

### Network Isolation

All embedded services bind to `127.0.0.1` only:

| Service        | Bind Address        |
|----------------|---------------------|
| qbittorrent-nox| 127.0.0.1:8091      |
| SABnzbd        | 127.0.0.1:8092      |
| Sonarr         | 127.0.0.1:8989      |
| Radarr         | 127.0.0.1:7878      |
| Lidarr         | 127.0.0.1:8686      |
| Whisparr       | 127.0.0.1:6969      |
| Prowlarr       | 127.0.0.1:9696      |
| Overseerr      | 127.0.0.1:5055      |
| FlareSolverr   | 127.0.0.1:8191      |

These ports are **never** exposed externally by default. Only the Nexus API (`:8080`) is externally accessible.

### Debug Mode

A future debug/development mode may allow optional exposure of native UIs. This requires:

- Explicit user opt-in via settings
- Clear warning in the UI
- Per-service toggle (not all-or-nothing)
- Automatic disable on container restart unless persisted

### API Key Management

- Internal service API keys are generated automatically during first-run or service enable.
- API keys are stored in `/config/nexus/secrets.yml`, which is:
  - Never committed to version control
  - Never logged
  - Never sent to the browser unless absolutely necessary
  - Masked in all log output
- Nexus adapters use these keys internally to communicate with services.
- The browser frontend communicates only with the Nexus API, never directly with internal services.

## Secret Handling

### What counts as a secret

- Service API keys (Sonarr, Radarr, etc.)
- Usenet provider credentials
- Indexer credentials / API keys
- qBittorrent WebUI password
- SABnzbd API key
- Nexus admin password hash
- Nexus API tokens
- GitHub tokens (development only)
- Any third-party service credentials

### Rules

1. **No secrets in the repository.** Ever. Not in code, not in configs, not in fixtures, not in docs.
2. **No secrets in Docker image layers.** Secrets are injected at runtime via volume mounts or environment variables.
3. **No secrets in logs.** All log output passes through a secret-masking filter.
4. **No secrets in API responses.** Masked with `••••••••` in UI and API.
5. **No default passwords.** First-run requires the user to set credentials.
6. **.gitignore** includes patterns for all secret files.

## Reverse Proxy Support

Nexus supports running behind a reverse proxy:

- Configurable base URL / path prefix
- Trusted proxy IP ranges
- X-Forwarded-For / X-Real-IP header support
- WebSocket proxy support for real-time updates

## Session Security

- Session tokens are cryptographically random
- HTTP-only, Secure (when HTTPS), SameSite=Lax cookies
- Configurable session timeout (default: 24 hours)
- Session invalidation on password change
- Rate limiting on login attempts

## Filesystem Security

- Nexus operates within its mounted volumes only
- No symlink following outside mounted paths
- No execution of user-uploaded content
- FFmpeg commands are constructed programmatically, never from raw user input
- Path traversal protection on all file operations

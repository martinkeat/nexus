# Nexus Test Strategy

## Test Layers

### 1. Unit Tests (`tests/unit/`)

- Test individual functions, classes, and adapters in isolation
- Mock all external dependencies (service APIs, filesystem, ffmpeg)
- Fast, deterministic, no side effects
- Run on every commit

### 2. Integration Tests (`tests/integration/`)

- Test adapter communication with service APIs
- Test settings persistence and retrieval
- Test service enable/disable lifecycle
- May require running service instances (in Docker or mocked)

### 3. API Adapter Tests (`tests/integration/adapters/`)

- Test each service adapter against the real service API schema
- Validate health check, config read/write, connectivity test
- Use recorded API responses (VCR-style) for offline runs

### 4. Settings Registry Tests (`tests/unit/settings/`)

- Test schema validation
- Test default values
- Test cross-validation rules
- Test migration from older schema versions

### 5. Filesystem Permission Tests (`tests/integration/filesystem/`)

- Test read/write on all expected mount points
- Test behaviour when paths are missing
- Test behaviour when permissions are wrong
- Use temporary directories for isolation

### 6. Docker Build Tests (`tests/docker/`)

- Build the image from a clean checkout
- Verify the image starts without errors
- Verify all service binaries are present
- Verify s6-overlay initialises correctly

### 7. Container Startup Tests (`tests/docker/`)

- Start container with clean config
- Start container with existing config
- Verify Nexus API responds on :8080
- Verify no native ports are exposed externally

### 8. Service Health Tests (`tests/integration/health/`)

- Verify each service health check returns correct state
- Test healthy, starting, stopped, disabled, error states
- Test health aggregation in the dashboard

### 9. UI Component Tests (`tests/e2e/`)

- Test critical UI flows (login, dashboard, settings)
- Test responsive layouts
- Test dark/light theme rendering
- Use browser automation (Playwright recommended)

### 10. End-to-End Browser Tests (`tests/e2e/`)

- Full workflow: login → enable service → configure → verify
- First-run wizard completion
- Download monitoring
- Transcoding trigger and status

### 11. Transcoding Dry-Run Tests (`tests/integration/transcoding/`)

- Use tiny fixture media files (see Fixtures section)
- Verify probe output parsing
- Verify profile selection logic
- Verify FFmpeg command generation (dry-run)
- Verify actual transcode of tiny files
- Verify output file integrity

### 12. GPU Detection Tests (`tests/integration/gpu/`)

- Test detection logic with mocked ffmpeg output
- Test capability card generation
- Test encoder validation against detected capabilities
- Test fallback behaviour

### 13. Security Tests (`tests/unit/security/`)

- Verify no secrets in log output
- Verify API key masking in responses
- Verify session token generation
- Verify login rate limiting
- Verify path traversal protection

### 14. Upgrade/Migration Tests (`tests/integration/migration/`)

- Test config schema migration between versions
- Test service config preservation across upgrades
- Test database migration

### 15. Backup/Restore Tests (`tests/integration/backup/`)

- Test backup creation
- Test restore from backup
- Verify all settings and state are preserved

### 16. Unraid Deployment Smoke Tests (`tests/docker/unraid/`)

- Deploy to assigned Unraid test path
- Verify container starts
- Verify GUI loads
- Verify folder permissions
- Clean up test container
- **Requires explicit user permission before execution**

## Test Fixtures (`tests/fixtures/`)

Pre-generated tiny media files for transcoding tests:

| Fixture                    | Format              | Size   | Purpose                          |
|----------------------------|---------------------|--------|----------------------------------|
| `sample_h264.mkv`         | H.264 + AAC         | ~100KB | Basic video transcode test       |
| `sample_hevc.mkv`         | HEVC + EAC3         | ~100KB | HEVC codec handling              |
| `sample_av1.mkv`          | AV1 + Opus          | ~100KB | AV1 codec handling (if possible) |
| `sample_aac.m4a`          | AAC audio           | ~50KB  | Audio-only transcode test        |
| `sample_flac.flac`        | FLAC audio          | ~50KB  | Lossless audio handling          |
| `sample_mp3.mp3`          | MP3 audio           | ~50KB  | Lossy audio handling             |
| `sample_ac3.mkv`          | H.264 + AC3         | ~100KB | AC3 audio transcode              |
| `sample_subtitles.mkv`    | H.264 + AAC + SRT   | ~100KB | Subtitle handling                |
| `sample_corrupt.mkv`      | Truncated file      | ~10KB  | Corrupt file detection           |
| `sample_unsupported.xyz`  | Random bytes        | ~10KB  | Unsupported format detection     |
| `sample_compliant.mkv`    | Matches default profile | ~100KB | Skip-if-compliant test       |

Fixtures are committed to the repository and must be tiny (under 1MB total).

## Pre-Commit Gates

Before every commit:

1. `ruff format` — Code formatting
2. `ruff check` — Linting
3. `mypy` — Type checking
4. `pytest tests/unit/` — Unit tests
5. Secret scan — No secrets staged
6. File scan — No generated junk files staged

## Pre-PR Gates

Before every pull request:

1. All pre-commit gates pass
2. Docker image builds from clean checkout
3. Container starts with clean config
4. Container starts with existing config
5. Nexus GUI loads in browser
6. Disabled services stay disabled
7. Enabled services start and report healthy
8. Folder permissions are verified
9. No native ports exposed externally
10. Settings save and reload correctly
11. First-run wizard completes successfully

## CI/CD

GitHub Actions workflows handle:

- Lint + type check on every push
- Unit tests on every push
- Docker build on every PR
- Container smoke test on every PR
- Security scan on every PR
- Release image build on tag

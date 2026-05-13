# Nexus Release Process

## Versioning

Nexus uses [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes to config schema, API, or container interface
- **MINOR**: New features, new service integrations, new profile options
- **PATCH**: Bug fixes, security patches, documentation corrections

## Branch Model

| Branch        | Purpose                                         |
|---------------|--------------------------------------------------|
| `main`        | Stable, release-ready code                       |
| `develop`     | Integration branch for next release              |
| `feature/*`   | Individual feature development                   |
| `fix/*`       | Bug fix branches                                 |
| `release/*`   | Release preparation and final testing            |

## Release Checklist

Before tagging a release:

### Code Quality
- [ ] All pre-commit gates pass
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Type checking passes
- [ ] Linting passes

### Docker
- [ ] Fresh clone → Docker build succeeds
- [ ] Container starts with clean config
- [ ] Container starts with existing config (upgrade test)
- [ ] All health checks report correctly

### Features
- [ ] First-run setup wizard works end-to-end
- [ ] Service toggle matrix tests pass
- [ ] Torrent-only mode works
- [ ] Usenet-only mode works
- [ ] Both-downloaders mode works
- [ ] No-GPU mode works
- [ ] GPU detection works (where hardware available)

### Transcoding
- [ ] Transcoding profile dry-run tests pass
- [ ] Tiny fixture transcodes succeed
- [ ] Arr import handoff works correctly
- [ ] Failed transcode handling works

### Security
- [ ] No secrets in repository
- [ ] No secrets in Docker image layers
- [ ] Secret masking in logs verified
- [ ] Login and session management tested
- [ ] No native ports exposed externally

### Documentation
- [ ] Architecture docs updated
- [ ] CHANGELOG.md updated
- [ ] README.md reflects current state
- [ ] Unraid deployment guide is accurate

### Release
- [ ] Version number updated
- [ ] CHANGELOG entry written
- [ ] Release branch merged to main
- [ ] Tag created: `vX.Y.Z`
- [ ] GitHub release published (if ready)

## Image Publishing

Docker images are published to GitHub Container Registry (ghcr.io):

```
ghcr.io/martinkeat/nexus:latest
ghcr.io/martinkeat/nexus:vX.Y.Z
ghcr.io/martinkeat/nexus:develop
```

Image publishing is **not enabled** until explicitly configured by the user.

## Rollback

If a release introduces a regression:

1. Pin to the previous version tag
2. Report the issue
3. Fix on a `fix/*` branch
4. Release a patch version

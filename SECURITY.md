# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability in Nexus, please report it responsibly:

1. **Do not** open a public GitHub issue for security vulnerabilities.
2. Contact the maintainer directly via GitHub private vulnerability reporting.
3. Include a clear description of the vulnerability and steps to reproduce.

## Security Design

- Nexus requires authentication on first run. No anonymous access by default.
- Internal service API keys are never exposed to the browser.
- All secrets are masked in logs and API responses.
- Native service UIs are bound to `127.0.0.1` and not exposed externally.
- No default passwords are shipped. Users must create credentials during setup.
- FFmpeg commands are constructed programmatically; no raw user input is executed.
- Path traversal protection is applied to all file operations.

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | ✅        |

## Dependencies

Nexus bundles third-party services. Security updates for embedded services are tracked and included in Nexus releases as they become available.

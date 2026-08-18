# Security

## Reporting a Vulnerability

If you discover a security issue in this project, please open a private
[security advisory](https://github.com/farhanrizve/research-tool/security/advisories/new)
or contact the maintainer directly. Do **not** open a public issue for
security vulnerabilities.

## Known Vulnerabilities

### `image-size` — DoS via crafted image files (no upstream patch yet)

- **Affected:** `image-size` `<= 2.0.2` (transitive dependency of `pptxgenjs`)
- **Advisories:**
  - [GHSA-w3rx-r6r6-pgpr](https://github.com/advisories/GHSA-w3rx-r6r6-pgpr) (CVE-2025-71330) — ICNS parser infinite loop
  - [GHSA-5p2g-fcmc-qvqq](https://github.com/advisories/GHSA-5p2g-fcmc-qvqq) (CVE-2025-71329) — JXL/HEIF parser infinite loop
- **Patched versions:** None published at this time.
- **Impact:** A crafted image buffer (ICNS/JXL/HEIF) can block the Node.js
  event loop indefinitely. Only reachable when generating PowerPoint files
  (`pptxgenjs`) from untrusted image input.
- **Status:** Tracked. `npm audit` reports 2 high-severity findings. The only
  automated "fix" (`npm audit fix --force`) downgrades `pptxgenjs` to a
  breaking older major version, so it is **not** applied.
- **Mitigation:** Do not feed untrusted/crafted image files into PPTX
  generation. Re-check `npm audit` periodically and upgrade `pptxgenjs` /
  `image-size` once a patched release is available.
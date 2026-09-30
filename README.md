# Internal Business Platform Security Assessment

A local-only web/API penetration-testing lab built with FastAPI, PostgreSQL, Nginx, and Docker.

This project simulates a small internal business platform and demonstrates the complete penetration-testing lifecycle:

- Scope definition
- Rules of engagement
- Asset discovery
- API reconnaissance
- Authentication and authorization testing
- Evidence collection
- Vulnerability reporting
- Secure remediation
- Regression testing
- Retesting
- Detection engineering

All testing is performed locally against intentionally controlled systems using synthetic data.

## Project Status

| Phase | Status |
|---|---|
| Local Docker environment | Complete |
| FastAPI application baseline | Complete |
| PostgreSQL database | Complete |
| Nginx reverse proxy | Complete |
| API baseline inspection | In progress |
| Authentication | Planned |
| Authorization testing | Planned |
| Security findings report | Planned |
| Remediation and retest | Planned |
| Detection engineering | Planned |

## Important Safety Notice

This project is intended for authorized local testing only.

The application runs on the owner's computer and uses synthetic data. Do not use the techniques, tools, or test cases from this repository against:

- Public websites
- Third-party APIs
- Employer or school systems
- Production applications
- Networks that you do not own
- Cloud environments without explicit written authorization

Do not expose the lab to the public Internet. Do not configure router port forwarding. Do not bind the application to `0.0.0.0` on the Windows host.

## Architecture

```text
                 Windows Host
                      |
             http://127.0.0.1:8080
                      |
                      v
              Nginx Reverse Proxy
                      |
                      v
                FastAPI API
                      |
                      v
                 PostgreSQL

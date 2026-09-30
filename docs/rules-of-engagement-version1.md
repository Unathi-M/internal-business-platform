# Rules of Engagement

## Internal Business Platform Security Assessment

**Document type:** Rules of Engagement (RoE)  
**Project:** Internal Business Platform Security Assessment  
**Assessment version:** Version 1 — Local Web/API Lab  
**Document version:** 1.0  
**Assessment status:** Authorized local testing  
**Tester and project owner:** `Unathi Manana`  
**Date created:** `2026-09-30`  
**Repository:** `internal-business-platform`  

---

## 1. Purpose

This document defines the authorization, scope, objectives, methods, limitations, safety controls, evidence-handling requirements, and reset procedures for the Version 1 assessment of the Internal Business Platform Security Assessment lab.

The assessment is performed against intentionally controlled systems running locally on the project owner's computer. The lab uses Docker Desktop, FastAPI, PostgreSQL, and Nginx. All application records are synthetic and created only for security-testing practice.

This document is designed to demonstrate professional penetration-testing preparation. It does not authorize testing of public websites, third-party services, employer systems, school systems, cloud accounts, or any other environment not explicitly listed here.

> **Authorization boundary:** Testing is authorized only against the local assets and addresses listed in this document.

---

## 2. Authorization

The project owner authorizes the tester named in this document to perform security testing against the local systems defined in the scope section.

The authorization applies only while the systems are running as part of this repository and only from the project owner's computer. The authorization does not extend to any system reachable through the same home network, VPN, public Internet, employer network, school network, or cloud account.

The tester must stop immediately if an action could affect a system outside the approved scope or if the tester cannot confidently determine that an action is authorized.

### Authorization statement

> I authorize the testing activities described in this document against the intentionally controlled local Docker lab defined in this repository. I understand that the authorization is limited to the listed local services, synthetic data, and approved testing activities.

**Authorized by:** `Your Name`  
**Role:** Project owner and tester  
**Date:** `YYYY-MM-DD`  
**Signature or acknowledgement:** `Your Name`  

---

## 3. Assessment objectives

The objectives of this assessment are to:

1. Define and verify the local API attack surface.
2. Review application behavior against the documented API contract.
3. Assess authentication and authorization controls when implemented.
4. Test object ownership and user-to-user data separation.
5. Review input validation and business-logic controls.
6. Identify information disclosure and unsafe error behavior.
7. Review the security configuration of the API, reverse proxy, and containers.
8. Collect reproducible and sanitized evidence.
9. Produce a professional security assessment report.
10. Implement remediation changes for confirmed findings.
11. Add regression tests for remediated behavior.
12. Retest the original findings and document the final status.

The project prioritizes sound assessment judgment and evidence quality over the number of tools or scanner alerts used.

---

## 4. Assessment type

This is a controlled local web and API security assessment with source-code and configuration review.

The assessment includes elements of:

- Black-box API testing through the local Nginx endpoint.
- Gray-box testing using documented test accounts and API documentation.
- White-box review of the application's source code and Docker configuration.
- Remediation verification and regression testing.

This is not a production penetration test, a compliance certification, a formal red-team exercise, or an assessment of Docker Desktop or the Windows host operating system.

---

## 5. In-scope assets

### 5.1 Primary target

The primary target is the local Nginx endpoint:

```text
http://127.0.0.1:8080
http://localhost:8080
```

Both addresses refer to the local application entry point. Testing must remain on the local computer.

### 5.2 Docker services

| Service | Container name | Internal address/port | Purpose | Scope |
|---|---|---|---|---|
| Nginx | `ibp-nginx` | Port `80` inside Docker | Reverse proxy and local entry point | In scope |
| FastAPI | `ibp-api` | Port `8000` inside Docker | Business application API | In scope through the application; direct testing only if separately documented |
| PostgreSQL | `ibp-postgres` | Port `5432` inside Docker | Application database | In scope for configuration review; direct database testing requires separate approval |

### 5.3 In-scope project files

The following project files are in scope for source and configuration review:

```text
docker-compose.yml
app/Dockerfile
app/main.py
app/requirements.txt
db/init.sql
nginx/default.conf
docs/*
tests/*
```

### 5.4 In-scope API endpoints

The initial baseline endpoints are:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Application health check |
| `GET` | `/api/v1/users` | List synthetic users |
| `GET` | `/api/v1/orders` | List synthetic orders |
| `POST` | `/api/v1/orders` | Create a synthetic order |
| `GET` | `/docs` | FastAPI interactive documentation |
| `GET` | `/openapi.json` | FastAPI OpenAPI document |

The endpoint list may change during project development. Any newly created local endpoint becomes in scope only after it is recorded in the test plan or inventory.

---

## 6. Out-of-scope assets and activities

The following are explicitly out of scope:

### 6.1 Out-of-scope systems

- Public websites and public IP addresses.
- Third-party APIs and services.
- Employer, client, school, or organization systems.
- Other devices on the home or office network.
- Home routers, wireless access points, printers, cameras, and smart devices.
- Corporate VPNs and connected networks.
- Production systems and real business applications.
- Cloud accounts, cloud control planes, and cloud-hosted resources.
- Public Docker registries other than downloading approved base images.
- Docker Desktop itself.
- The Windows host operating system.
- Hypervisor management interfaces.
- Any container not defined in this repository.
- Any database, service, or application not listed in the scope.

### 6.2 Out-of-scope activities

The following activities are prohibited:

- Denial-of-service or stress testing.
- High-volume fuzzing that could exhaust host resources.
- Password spraying or credential stuffing.
- Brute-force attacks against accounts.
- Credential theft or collection from the host.
- Malware execution.
- Persistence or startup modification.
- Container breakout attempts.
- Access to the Docker socket from a vulnerable application.
- Host filesystem access or host privilege escalation.
- Destructive database operations.
- Deletion or modification of host files.
- Real data exfiltration.
- Requests to external webhook, callback, email, SMS, payment, or notification services.
- Testing public cloud metadata services.
- Phishing or social engineering.
- Testing nearby wireless networks or devices.
- Publishing secrets, credentials, or harmful exploit details.

---

## 7. Environment and architecture

The lab runs locally on the project owner's Windows computer using Docker Desktop and WSL 2.

The intended request flow is:

```text
Browser or PowerShell
        |
        | 127.0.0.1:8080
        v
Nginx reverse proxy
        |
        | Docker network
        v
FastAPI application
        |
        | Docker network
        v
PostgreSQL database
```

The only service published to the Windows host is Nginx on:

```text
127.0.0.1:8080
```

The API and PostgreSQL services are intended to remain internal to the Docker network.

### 7.1 Network restrictions

- Do not bind the application to a public or LAN-facing address.
- Do not change the host binding to `0.0.0.0:8080:80`.
- Do not configure router port forwarding.
- Do not expose PostgreSQL to the Windows host unless separately authorized.
- Do not expose the Docker API, Docker socket, Nginx management interface, or database administration interface.
- Verify the active port mapping before testing.
- Stop testing if a request appears to leave the local machine.

### 7.2 Pre-test network verification

Before testing, verify that the intended local port is available:

```powershell
Test-NetConnection localhost -Port 8080
```

Review the published Docker ports:

```powershell
docker compose ps
```

The expected Nginx mapping is similar to:

```text
127.0.0.1:8080->80/tcp
```

Unexpected published ports must be investigated before testing continues.

---

## 8. Test accounts and synthetic data

The lab uses synthetic identities only.

| Account | Role | Purpose |
|---|---|---|
| `alice@example.test` | `user` | Standard user testing |
| `bob@example.test` | `user` | User-to-user separation testing |
| `admin@example.test` | `admin` | Administrative authorization testing |

The `.test` domain is used for documentation and local testing. It does not represent real email accounts.

### 8.1 Synthetic data requirements

The lab may contain:

- Fictional user records.
- Fictional orders.
- Fictional invoice descriptions.
- Synthetic identifiers.
- Test tokens created only for the lab.
- Local logs generated by the application.

The lab must not contain:

- Real passwords.
- Real API keys.
- Production tokens.
- Customer information.
- Personal data.
- Banking or payment information.
- Employer or client data.
- Real certificates or private keys.
- Credentials reused from another system.

---

## 9. Authorized testing activities

The following activities are authorized when performed only against the in-scope local target:

### 9.1 Reconnaissance and discovery

- Review the Swagger documentation.
- Review the OpenAPI document.
- Browse the local application.
- Identify documented routes and methods.
- Compare documented routes with observed application behavior.
- Perform low-rate endpoint discovery against `127.0.0.1:8080`.
- Review response headers and error messages.
- Review local Docker service configuration.

### 9.2 Web/API testing

- Test HTTP methods and status codes.
- Test missing, malformed, and unexpected input values.
- Test authentication behavior after authentication is implemented.
- Test session and token behavior after those features are implemented.
- Test object-level authorization.
- Test function-level authorization.
- Test user and administrator separation.
- Test customer and order ownership.
- Test excessive data exposure.
- Test security headers.
- Test error handling.
- Test rate limiting only at a low, non-disruptive level.
- Test business workflows using synthetic data.

### 9.3 Source and configuration review

- Review Python source code.
- Review SQL statements and database initialization.
- Review Dockerfiles and Compose configuration.
- Review Nginx configuration.
- Review dependency versions.
- Run local source and dependency scanners.
- Review the generated OpenAPI document.

### 9.4 Remediation and retesting

- Modify the application or configuration to fix confirmed local findings.
- Add unit or integration tests.
- Rebuild the Docker images.
- Reset the database when required.
- Repeat the original safe test.
- Document whether the finding is fixed, partially fixed, accepted, or not retested.

---

## 10. Authorized tools

The following tools may be used against the local lab:

| Tool | Approved purpose | Restriction |
|---|---|---|
| Browser | Browse local application and Swagger UI | Local target only |
| PowerShell | Repeatable HTTP requests and environment checks | Local target only |
| `curl` or HTTPie | Manual and scripted API requests | Local target only |
| OWASP ZAP | Local web/API discovery and controlled scanning | Low rate; local target only |
| Burp Suite Community Edition | Request interception and manual replay | Local target only |
| Nmap | Local service discovery | Restrict to approved local addresses |
| Semgrep | Source-code security checks | Local repository only |
| Trivy | Local image and dependency review | Local images and repository only |
| Gitleaks | Secret scanning | Local repository only |
| Docker Compose | Start, stop, reset, and rebuild the lab | This project only |
| Git | Version control and evidence history | This project only |

Tool output is considered evidence or a lead, not automatically a confirmed vulnerability.

---

## 11. Rate limits and test restrictions

Testing must remain low impact.

The following restrictions apply:

- No denial-of-service testing.
- No stress testing.
- No resource-exhaustion testing.
- No high-volume automated scanning.
- No uncontrolled recursion or infinite requests.
- No payloads designed to damage the host or database.
- No tests that intentionally fill disk space or exhaust memory.
- No more than five requests per second for automated endpoint discovery unless a later test plan explicitly approves a lower-impact alternative.
- Use short timeouts for scripts and scanners.
- Exclude unrelated paths from automated tools.
- Stop any scanner that produces unexpected traffic or instability.
- Confirm the target URL before starting each automated tool.

For this small lab, lower request rates are preferred.

---

## 12. Testing methodology

Testing will follow a staged process.

### Phase 1 — Pre-engagement and scope confirmation

- Review this document.
- Confirm the target URL.
- Confirm that Docker services are running.
- Confirm that only intended ports are published.
- Confirm that test data is synthetic.
- Record the assessment date and tool versions.

### Phase 2 — Reconnaissance

- Review the API documentation.
- Identify routes, methods, parameters, and response fields.
- Review headers, errors, and status codes.
- Record the asset inventory.
- Create an API coverage matrix.

### Phase 3 — Threat modeling

- Identify users, roles, objects, and trust boundaries.
- Identify sensitive actions and data.
- Identify expected ownership relationships.
- Identify possible authorization boundaries.
- Document assumptions and testing limitations.

### Phase 4 — Vulnerability analysis

- Test authentication and authorization.
- Test input validation.
- Test business logic.
- Test configuration and information disclosure.
- Review source code and dependencies.
- Use scanners only to support manual investigation.

### Phase 5 — Safe validation

- Reproduce suspected findings with synthetic data.
- Capture only the evidence necessary to prove the issue.
- Avoid destructive actions.
- Avoid real outbound requests.
- Record the exact preconditions and expected result.

### Phase 6 — Reporting

- Rank findings by risk and practical impact.
- Explain the root cause.
- Provide developer-ready remediation.
- State limitations and blocked tests.
- Separate confirmed findings from hypotheses and scanner results.

### Phase 7 — Remediation and retesting

- Implement the fix.
- Add a regression test.
- Rebuild from a known-good state.
- Repeat the original test.
- Record the final status.

---

## 13. Evidence-handling requirements

Evidence must be collected carefully and kept proportional to the finding.

### 13.1 Evidence may include

- Sanitized HTTP requests and responses.
- Swagger screenshots.
- Browser screenshots.
- PowerShell output.
- Application logs.
- Nginx access logs.
- Docker status output.
- Request IDs.
- Tool names and versions.
- Source-code line references.
- Database results containing synthetic data.
- Hashes of selected evidence files.

### 13.2 Evidence register fields

Each test case should be recorded with:

| Field | Description |
|---|---|
| Test ID | Unique identifier, such as `API-AUTHZ-001` |
| Date/time | Time of the test |
| Tester | Person performing the test |
| Target | Local hostname and endpoint |
| Account | Synthetic account used |
| Preconditions | Required setup before the test |
| Tool/version | Tool used and version |
| Expected result | Expected secure behavior |
| Actual result | Observed behavior |
| Evidence reference | Screenshot, log, request, or hash |
| Finding status | Hypothesis, blocked, confirmed, or not applicable |
| Cleanup status | Whether the environment was restored |

### 13.3 Evidence minimization

Collect only what is needed to prove the result. Redact:

- Tokens.
- Passwords.
- Secret values.
- Personal information.
- Host identifiers unrelated to the lab.
- Unnecessary command history.
- Unnecessary exploit details.

### 13.4 Public repository requirements

Before pushing changes to GitHub:

- Review every changed file.
- Search for secrets and tokens.
- Remove real or sensitive data.
- Remove unneeded logs and packet captures.
- Confirm that all examples use synthetic values.
- Confirm that the README states the authorization boundary.

Use:

```powershell
git status
git diff
gitleaks detect --source .
```

if Gitleaks is installed locally.

---

## 14. Finding-confirmation standard

A scanner alert, theoretical attack path, or suspicious behavior is not automatically a confirmed vulnerability.

A finding is confirmed only when:

1. The behavior occurs within the authorized local scope.
2. The preconditions are documented.
3. The behavior can be reproduced safely.
4. The evidence supports the conclusion.
5. The security impact is explained.
6. The root cause is understood well enough to recommend a fix.
7. The limitations are documented.

Each confirmed finding must contain:

- Finding identifier.
- Finding title.
- Affected endpoint or component.
- Severity and severity rationale.
- Preconditions.
- Safe reproduction steps.
- Sanitized evidence.
- Expected secure behavior.
- Actual observed behavior.
- Business or security impact.
- Root cause.
- Recommended remediation.
- Regression test.
- Retest status.
- Limitations.

Classify results as one of the following:

- `Confirmed` — manually validated in the authorized lab.
- `Scanner lead` — reported by a tool and not yet manually confirmed.
- `Theoretical` — possible based on design review but not demonstrated.
- `Blocked` — attempted safely but prevented by a control or limitation.
- `Not applicable` — not relevant to this version of the application.
- `False positive` — investigated and determined not to be a vulnerability.

---

## 15. Stop conditions

Testing must stop immediately if any of the following occurs:

- Traffic is observed leaving the local computer.
- A non-local target appears in scanner results.
- A public IP address or third-party hostname is identified as a target.
- Real personal, financial, production, employer, or customer data is discovered.
- A test could damage the database.
- A test could modify the Windows host.
- A test could access the Docker socket or host filesystem.
- The host becomes unstable, unresponsive, or unusually slow.
- Containers repeatedly crash or consume excessive resources.
- A scanner behaves outside the defined rate limit.
- An unexpected external callback, email, SMS, or network connection is attempted.
- The tester is uncertain whether an action is authorized.
- The scope or target cannot be verified.

When a stop condition occurs:

1. Stop the current tool or request.
2. Record the time and action being performed.
3. Preserve relevant local logs.
4. Stop or isolate the affected container if necessary.
5. Check for unexpected network connections.
6. Restore the lab to a known-good state.
7. Document the incident and impact.
8. Update this document or the test plan before continuing.

---

## 16. Backup, reset, and rollback

### 16.1 Normal shutdown

Stop the application stack:

```powershell
docker compose down
```

### 16.2 Database reset

Reset the synthetic PostgreSQL data:

```powershell
docker compose down -v
docker compose up -d --build
```

The `-v` option removes the project's local PostgreSQL volume. The database is then recreated using `db/init.sql`.

### 16.3 Complete project cleanup

To remove the project's containers and network:

```powershell
docker compose down --remove-orphans
```

To inspect remaining project containers:

```powershell
docker compose ps -a
```

### 16.4 Git rollback

Before major changes, create a Git commit:

```powershell
git add .
git commit -m "Create known-good assessment baseline"
```

View previous commits:

```powershell
git log --oneline --max-count=10
```

Do not reset or delete work without first checking whether evidence or documentation must be preserved.

---

## 17. Incident handling

If unexpected behavior occurs during testing, the tester will:

1. Stop testing immediately.
2. Stop the affected scanner or script.
3. Record the test ID, command, endpoint, date, and time.
4. Save relevant application and Docker logs.
5. Check whether any traffic left the local system.
6. Stop the affected service if necessary.
7. Restore the environment from the known-good state.
8. Review the cause before resuming.
9. Document the event in the assessment notes.
10. Update the RoE or test plan if a control was insufficient.

Potentially sensitive or unexpected events must not be hidden from the project record, even when no damage occurred.

---

## 18. Reporting requirements

The final assessment report will contain:

1. Executive summary.
2. Assessment objectives.
3. Scope and authorization.
4. Environment and architecture.
5. Methodology.
6. Tools and versions.
7. Test limitations.
8. Asset and endpoint inventory.
9. Test coverage matrix.
10. Risk summary.
11. Detailed findings.
12. Evidence references.
13. Remediation recommendations.
14. Regression-test results.
15. Retest results.
16. Residual risk.
17. Appendix containing sanitized evidence and test notes.

The report must clearly distinguish:

- Confirmed vulnerabilities.
- Scanner results.
- Theoretical attack paths.
- Blocked tests.
- False positives.
- Areas not assessed.

The report must not claim that the application is secure merely because no finding was identified.

---

## 19. Change control

Changes to the following items must be documented before testing continues:

- Target endpoints.
- Docker services.
- Published ports.
- Database schema.
- Authentication or authorization behavior.
- Test accounts.
- Testing tools.
- Automated scan rate.
- Evidence-storage location.
- Scope or out-of-scope boundaries.

For significant changes:

1. Update this document or the test plan.
2. Commit the change to Git.
3. Rebuild the lab.
4. Recheck published ports.
5. Confirm the target URL.
6. Record the new assessment version.

---

## 20. Assessment limitations

This assessment is limited by the local training environment.

The results do not prove that:

- The application is secure in production.
- The same behavior exists in another application.
- The Docker platform or Windows host is secure.
- Cloud services are secure.
- Detection rules work in every SIEM.
- The test covers every OWASP category.
- The testing represents a full enterprise penetration test.
- The application has no undiscovered vulnerabilities.

The results apply only to the application version, Docker configuration, test data, and test period documented in the project repository.

---

## 21. Completion criteria

The Version 1 assessment is complete when:

- The scope and RoE are committed to Git.
- The application architecture is documented.
- The endpoint inventory is complete.
- The baseline behavior is recorded.
- The planned test cases are executed or marked as blocked/not applicable.
- Findings are manually validated.
- Scanner output is separated from confirmed findings.
- Remediation is implemented for confirmed findings.
- Regression tests are added.
- Original findings are retested.
- A final report is written.
- Evidence is sanitized.
- The repository contains no secrets or real sensitive data.
- The lab can be reset from documented commands.

---

## 22. Approval and sign-off

### Authorization approval

**Authorized by:** `Your Name`  
**Role:** Project owner and tester  
**Date:** `YYYY-MM-DD`  
**Signature or acknowledgement:** `Your Name`  

### Assessment completion

**Assessment completed by:** `Your Name`  
**Completion date:** `YYYY-MM-DD`  
**Final report location:** `docs/technical-report.md`  
**Retest memo location:** `docs/retest-memo.md`  
**Final Git commit:** `commit-hash`  

---

## 23. Version history

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | `YYYY-MM-DD` | `Your Name` | Initial Version 1 local web/API rules of engagement |

---

## 24. Tester acknowledgement

I acknowledge that I will test only the systems explicitly listed in this document, use synthetic data, follow the prohibited-activity restrictions, preserve evidence responsibly, and stop when the scope or safety boundary is uncertain.

**Name:** `Your Name`  
**Date:** `YYYY-MM-DD`  
**Acknowledgement:** `I agree to these rules of engagement.`

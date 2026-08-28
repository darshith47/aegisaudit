# AegisAudit Security Policy

## Security Architecture & Controls

AegisAudit is engineered with strict defensive security controls to ensure all security assessments remain authorized and constrained within permitted parameters:

1. **Centralized Scope Engine**: Every network assessment job is evaluated against a pre-authorized Scope policy before parameter execution. Targets outside authorized subnets, IPs, domains, ports, or protocols are immediately rejected (`JobStatus.REJECTED_OUT_OF_SCOPE`).
2. **Role-Based Access Control (RBAC)**: Fine-grained permissions distinguish `ADMIN`, `AUDITOR`, and `VIEWER` roles to prevent unauthorized job creation or scope modifications.
3. **No Arbitrary Shell Execution**: Engine adapters use typed argument lists (`List[str]`) rather than raw shell strings (`shell=True`), eliminating command injection vulnerabilities.
4. **Sensitive Data Masking**: Recovered credentials and test fixtures are masked in logs and reports.
5. **Mock Mode Safety (`MOCK_ENGINE=true`)**: Simulated execution mode prevents accidental live network traffic during development, testing, and portfolio demonstrations.

---

## Reporting a Vulnerability

We take the security of AegisAudit seriously.

Please do not publicly disclose a suspected security vulnerability before contacting the maintainers.

Until a dedicated security contact email is configured, please report any suspected vulnerability by opening a **Private Vulnerability Report** through the repository's supported GitHub Security Advisory tab.

Please include:
* Description of the vulnerability
* Steps to reproduce the issue
* Potential impact

We will investigate and respond promptly.

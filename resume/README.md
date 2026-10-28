# Cybersecurity Resume Guide & Tailoring Playbook

This folder contains two synchronized resume formats engineered for cybersecurity and application security job applications:
- **`resume.html`**: A modern, styled, printable HTML resume designed to produce a pixel-perfect, single-page A4 PDF using your web browser's "Print to PDF" feature.
- **`resume.md`**: A clean, structured Markdown resume ideal for plain-text ATS application portals (e.g., Workday, Greenhouse, Lever).

---

## 🎯 5 Tips for Tailoring This Resume to Any Cybersecurity Job Description

### Tip 1: Mirror the Job Posting’s Exact Technical Keywords (Beat the ATS)
Applicant Tracking Systems (ATS) scan resumes for exact keyword matches before a human recruiter ever sees them.
- **How to apply**: Analyze the target job description for recurring keywords (e.g., `"OWASP Top 10"`, `"Vulnerability Assessment"`, `"Python"`, `"Docker"`, `"REST APIs"`, `"RBAC"`, `"Penetration Testing"`, or `"CI/CD"`).
- Ensure that those exact terms appear prominently in your **Technical Skills** section and within the **AegisAudit** bullet points.

### Tip 2: Quantify Your Accomplishments (Fill the `[ADD METRIC]` Placeholders)
Recruiters and engineering managers look for measurable impact rather than passive task descriptions.
- **Where to edit**: Search for every occurrence of `[ADD METRIC]` in `resume.html` and `resume.md`.
- **Examples to substitute**:
  - *"cutting manual documentation time by **80%**"*
  - *"achieving **80%+** backend automated test coverage with Pytest"*
  - *"auditing **25+** simulated internal services in under **3 minutes**"*
  - *"eliminating **100%** of command-injection vectors through typed argument vectors"*

### Tip 3: Adapt the Professional Summary to the Specific Security Track
A generic summary gets skipped. Customize the 3-line summary to speak directly to the job specialization:
- **For Application Security (AppSec) Roles**: Emphasize secure-by-design API architecture, defensive coding, input sanitization, and automated CI/CD security pipelines.
- **For Penetration Testing / Offensive Roles**: Emphasize hands-on experience with Kali Linux, Hashcat, John the Ripper, Hydra, network authentication auditing, and proof-of-concept testing.
- **For SOC / Security Analyst Roles**: Emphasize log integrity, tamper-proof audit trails, forensic evidence preservation (SHA-256), and scope verification.

### Tip 4: Preserve the 1-Page A4 Layout When Saving to PDF
`resume.html` is specifically engineered with CSS `@page` media queries so it renders seamlessly on a single A4 sheet without overflowing to page two.
- **How to generate your PDF**:
  1. Open `resume/resume.html` in Google Chrome, Microsoft Edge, or Mozilla Firefox.
  2. Press **Ctrl + P** (Windows) or **Cmd + P** (Mac).
  3. Set **Destination**: *"Save as PDF"*.
  4. Set **Paper Size**: *"A4"*.
  5. Set **Margins**: *"None"* or *"Default"*.
  6. Ensure **"Background graphics"** is checked.
  7. Verify the print preview is exactly **1 page**, then click **Save**.

### Tip 5: Prepare STAR Stories for Every Resume Bullet Point
Every bullet on this resume represents a real architectural decision in AegisAudit. Practice explaining them using the **STAR** method (Situation, Task, Action, Result):
- **Situation**: Credential security audits often run the risk of testing systems outside client authorization.
- **Task**: Prevent any security tool from firing against unapproved targets without relying on tester memory.
- **Action**: Built a centralized Python Scope Engine that checks target IPs against approved CIDR subnets before dispatching jobs.
- **Result**: Completely blocked out-of-scope executions and recorded rejections to an immutable compliance audit trail.

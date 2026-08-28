# AegisAudit — Portfolio & LinkedIn Presentation Guide

## Project Description

> AegisAudit is an authorized credential-security assessment platform designed to centralize assessment scope policy, authorization, security-engine orchestration, background job management, evidence collection, and compliance security reporting.
>
> The platform architecture uses a modular engine-adapter model so security tools (such as offline password auditing and network authentication testing engines) can be safely integrated behind a centralized target-scope validation layer.

---

## Key Technical Highlights

- **Modular Security Engine Adapter Architecture**: Designed a flexible Python adapter system for standardizing security tool parameters, command building, and output parsing.
- **Centralized Scope Validation Engine**: Implemented strict pre-execution subnet, IP, domain, port, and protocol verification to prevent out-of-scope security testing.
- **Background Job Orchestration**: Built background job management and lifecycle tracking for security assessment tasks.
- **Audit Logging & Evidence Integrity**: Added immutable audit logging and SHA256 hashing for raw tool execution output.
- **Safe Demonstration Mock Mode**: Designed a simulation mode (`MOCK_ENGINE=true`) enabling safe local execution and UI demonstrations without live network traffic.
- **Typed Parameter Sanitation**: Implemented argument vector construction (`List[str]`) eliminating arbitrary shell command execution risks.
- **Executive Security Reporting**: Built automatic Markdown and HTML report generation summarizing assessment findings and remediation steps.

---

## Technology Stack

- **Backend**: Python 3.10+, FastAPI, Pydantic, SQLAlchemy 2.0, Alembic, PyJWT, Passlib, Pytest, Uvicorn
- **Frontend**: React 18, TypeScript, Vite, Lucide Icons, CSS3 Design System
- **Databases & Caching**: PostgreSQL, SQLite, Redis
- **Containerization & Dev Tools**: Docker, Docker Compose, Ruff, Black, MyPy
- **Security Tools Integrated**: Hashcat, John the Ripper, Hydra

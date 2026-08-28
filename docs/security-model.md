# AegisAudit — Security Model & Scope Enforcement

## Executive Summary

The primary design principle of AegisAudit is **Authorized Security Testing Only**. No security engine adapter or assessment task can execute against an unvalidated or out-of-scope target.

---

## Centralized Execution Pipeline

```text
Authentication
      ↓
RBAC (Admin / Auditor / Viewer)
      ↓
Assessment Authorization
      ↓
Engine Allowlist Verification
      ↓
Centralized Scope Engine Validation
      ↓
Protocol Allowlist Validation
      ↓
Port Allowlist Validation
      ↓
Resource Policy Check
      ↓
Engine Parameter Sanitation
      ↓
Job Execution Queue
      ↓
Isolated Worker Execution
      ↓
Security Engine Adapter
      ↓
Results & Evidence SHA256 Integrity Hash
      ↓
Immutable Audit Log
```

---

## Strict Rules & Governance

1. **No Arbitrary Shell Execution**: Commands are constructed as explicit argument vectors (`List[str]`). Shell string expansion (`shell=True`) is strictly prohibited.
2. **Scope Pre-Execution Gate**: `ScopeEngine.validate_target()` is invoked *before* any job transitions to `RUNNING`. If validation fails, the job status is immediately set to `JobStatus.REJECTED_OUT_OF_SCOPE`.
3. **No Out-of-Scope Bypass**: Network-capable engine adapters (such as Hydra) derive their target validation directly from the central Scope policy and cannot bypass authorization.
4. **Mock Execution Mode (`MOCK_ENGINE=true`)**: Allows safe platform demonstrations without generating live network traffic or interacting with external tool binaries.

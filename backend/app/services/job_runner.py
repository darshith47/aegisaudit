import hashlib
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.config import settings
from app.models.job import Job, JobStatus
from app.models.assessment import Assessment, AssessmentStatus
from app.models.evidence import Evidence
from app.models.finding import Finding, FindingSeverity
from app.models.audit import AuditLog
from app.adapters.registry import engine_registry


class JobRunnerService:
    """Orchestrates security assessment job execution & mock mode processing."""

    @staticmethod
    def execute_job(db: Session, job_id: int, user_id: int = None) -> Job:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise ValueError(f"Job #{job_id} not found.")

        assessment = db.query(Assessment).filter(Assessment.id == job.assessment_id).first()
        if not assessment:
            job.status = JobStatus.FAILED
            job.output = "Error: Parent assessment not found."
            db.commit()
            return job

        scope = assessment.scope
        adapter = engine_registry.get_adapter(job.engine_name)
        if not adapter:
            job.status = JobStatus.FAILED
            job.output = f"Error: Security engine adapter '{job.engine_name}' is not supported or not installed."
            db.commit()
            return job

        # Step 1: Centralized Scope Engine Check
        is_allowed, scope_reason = adapter.validate_scope(
            scope=scope,
            target=assessment.target,
            parameters=job.parameters or {}
        )

        if not is_allowed:
            job.status = JobStatus.REJECTED_OUT_OF_SCOPE
            job.progress = 0.0
            job.output = f"REJECTED BY CENTRALIZED SCOPE ENGINE: {scope_reason}"
            job.completed_at = datetime.utcnow()
            
            # Log audit event
            audit = AuditLog(
                user_id=user_id,
                action="JOB_REJECTED_OUT_OF_SCOPE",
                resource=f"job:{job.id}",
                details={"target": assessment.target, "scope_id": scope.id, "reason": scope_reason}
            )
            db.add(audit)
            db.commit()
            return job

        # Update Job status to RUNNING
        job.status = JobStatus.RUNNING
        job.started_at = datetime.utcnow()
        job.progress = 0.1
        assessment.status = AssessmentStatus.IN_PROGRESS
        db.commit()

        # Step 2: Run in Mock Mode (default) or real execution
        if settings.MOCK_ENGINE or job.mock_mode:
            raw_output, mock_findings = adapter.generate_mock_results(
                target=assessment.target,
                parameters=job.parameters or {}
            )
        else:
            # Live execution fallback (safety dry-run)
            cmd = adapter.build_command(assessment.target, job.parameters or {})
            raw_output = f"[LIVE EXECUTION COMMAND]: {' '.join(cmd)}\n[INFO] Real execution dry-run completed."
            mock_findings = adapter.parse_output(raw_output)

        # Step 3: Create Evidence entry with SHA256 integrity hash
        sha256_hash = hashlib.sha256(raw_output.encode("utf-8")).hexdigest()
        evidence = Evidence(
            raw_output=raw_output,
            sha256_hash=sha256_hash,
            collected_at=datetime.utcnow()
        )
        db.add(evidence)
        db.flush()

        # Step 4: Create Findings
        for mf in mock_findings:
            finding = Finding(
                assessment_id=assessment.id,
                title=mf["title"],
                severity=FindingSeverity[mf["severity"]],
                vulnerability_type=mf["vulnerability_type"],
                target=mf["target"],
                details=mf["details"],
                remediation=mf["remediation"],
                evidence_id=evidence.id,
                is_mock=settings.MOCK_ENGINE
            )
            db.add(finding)

        # Update Job & Assessment Status
        job.status = JobStatus.COMPLETED
        job.progress = 1.0
        job.output = raw_output
        job.completed_at = datetime.utcnow()
        assessment.status = AssessmentStatus.COMPLETED

        # Create Audit Log record
        audit = AuditLog(
            user_id=user_id,
            action="JOB_COMPLETED",
            resource=f"job:{job.id}",
            details={
                "engine": job.engine_name,
                "target": assessment.target,
                "findings_count": len(mock_findings),
                "evidence_hash": sha256_hash
            }
        )
        db.add(audit)
        db.commit()
        db.refresh(job)
        return job

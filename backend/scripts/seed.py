"""
AegisAudit Demonstration Seed Script
------------------------------------
Populates the database with default demonstration accounts and sample
authorized assessment scopes for local evaluation and UI walkthroughs.

DEMO CREDENTIALS:
- Admin:   username=admin   password=DemoAdmin2026!
- Auditor: username=auditor password=DemoAuditor2026!
- Viewer:  username=viewer  password=DemoViewer2026!
"""

import os
import sys

# Add parent directory to path so script can be run standalone
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.security import get_password_hash
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.assessment import Assessment, AssessmentStatus
from app.models.finding import Finding, FindingSeverity
from app.models.scope import Scope
from app.models.user import User, UserRole


def seed_database() -> None:
    print("[*] Initializing AegisAudit database schema...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 1. Seed Demo Accounts
        demo_accounts = [
            ("admin", "admin@aegisaudit.local", "DemoAdmin2026!", UserRole.ADMIN),
            ("auditor", "auditor@aegisaudit.local", "DemoAuditor2026!", UserRole.AUDITOR),
            ("viewer", "viewer@aegisaudit.local", "DemoViewer2026!", UserRole.VIEWER),
        ]

        print("[*] Seeding role-based demo accounts...")
        for username, email, raw_pwd, role in demo_accounts:
            existing = db.query(User).filter(User.username == username).first()
            if not existing:
                user = User(
                    username=username,
                    email=email,
                    hashed_password=get_password_hash(raw_pwd),
                    role=role,
                    is_active=True,
                )
                db.add(user)
                print(f"    [+] Created {role.value.upper()} user: {username}")
            else:
                # Update password hash to ensure consistency
                existing.hashed_password = get_password_hash(raw_pwd)
                print(f"    [=] User {username} exists (password verified).")

        db.commit()

        # 2. Seed Demonstration Authorized Scope
        print("[*] Seeding authorized demonstration scope...")
        scope = db.query(Scope).filter(Scope.name == "Internal Lab Network Scope").first()
        if not scope:
            scope = Scope(
                name="Internal Lab Network Scope",
                description="Authorized penetration testing lab scope for credential security audits",
                allowed_targets="10.0.0.0/24, 192.168.1.0/24, 127.0.0.1, localhost, demo.lab",
                allowed_ports="22,80,443,3389,8080",
                allowed_protocols="ssh,http,https,rdp,ftp",
            )
            db.add(scope)
            db.commit()
            db.refresh(scope)
            print("    [+] Created demonstration scope: 'Internal Lab Network Scope'")
        else:
            print("    [=] Demonstration scope already present.")

        # 3. Seed Sample Completed Assessment & Mock Findings
        sample_assessment = (
            db.query(Assessment).filter(Assessment.title == "Lab SSH Credential Audit").first()
        )
        if not sample_assessment:
            sample_assessment = Assessment(
                title="Lab SSH Credential Audit",
                description="Automated credential hygiene assessment against internal staging server",
                target="10.0.0.15",
                engine="hydra",
                status=AssessmentStatus.COMPLETED,
                scope_id=scope.id,
            )
            db.add(sample_assessment)
            db.commit()
            db.refresh(sample_assessment)

            finding = Finding(
                assessment_id=sample_assessment.id,
                title="Default / Weak SSH Credential Identified",
                severity=FindingSeverity.HIGH,
                vulnerability_type="Weak Credentials",
                target="10.0.0.15:22 (ssh)",
                details="Simulated discovery: identified credentials 'admin:password123' via authorized dictionary audit.",
                remediation="Enforce SSH key-based authentication and disable password-based root/administrative login.",
                is_mock=True,
            )
            db.add(finding)
            db.commit()
            print("    [+] Seeded sample assessment and mock finding for UI demonstration.")

        print("\n=======================================================")
        print("  AegisAudit Demonstration Environment Ready!")
        print("=======================================================")
        print("  Roles & Accounts:")
        print("  - Admin:   username: admin   | password: DemoAdmin2026!")
        print("  - Auditor: username: auditor | password: DemoAuditor2026!")
        print("  - Viewer:  username: viewer  | password: DemoViewer2026!")
        print("=======================================================\n")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

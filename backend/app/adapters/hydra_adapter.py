from typing import Any, Dict, List, Tuple

from app.adapters.base import BaseEngineAdapter


class HydraAdapter(BaseEngineAdapter):
    """Hydra Network Authentication Assessment Adapter."""

    def __init__(self) -> None:
        super().__init__(name="Hydra", category="Authentication Audit", requires_network=True)

    def build_command(self, target: str, parameters: Dict[str, Any]) -> List[str]:
        service = str(parameters.get("service", "ssh")).lower()
        user = str(parameters.get("username", "admin"))
        wordlist = str(parameters.get("wordlist", "/usr/share/wordlists/passwords.txt"))
        port = parameters.get("port")

        cmd = ["hydra", "-l", user, "-P", wordlist]
        if port:
            cmd.extend(["-s", str(port)])
        cmd.extend([target, service])
        return cmd

    def parse_output(self, raw_output: str) -> List[Dict[str, Any]]:
        findings = []
        for line in raw_output.strip().splitlines():
            if "[22][ssh]" in line or "[80][http]" in line or "host:" in line.lower():
                findings.append(
                    {
                        "title": "Valid Network Credentials Identified (Hydra)",
                        "severity": "CRITICAL",
                        "vulnerability_type": "Weak Service Authentication",
                        "target": line.strip(),
                        "details": f"Hydra successfully authenticated against target service: {line.strip()}",
                        "remediation": "Disable default password login, enforce public key authentication, and deploy fail2ban / IP rate limiting.",
                    }
                )
        return findings

    def generate_mock_results(
        self, target: str, parameters: Dict[str, Any]
    ) -> Tuple[str, List[Dict[str, Any]]]:
        service = str(parameters.get("service", "ssh")).upper()
        port = parameters.get("port", 22)

        mock_output = (
            f"[DEMO / MOCK] Hydra v9.5 initialized for target {target}:{port} ({service}).\n"
            "[DEMO / MOCK] Scope validation check passed prior to connection.\n"
            "[DEMO / MOCK] Attacking 1 target, 1 service, 100 credentials per task.\n"
            f"[DEMO / MOCK] [{port}][{service.lower()}] host: {target}   login: admin   password: Password123!\n"
            "[DEMO / MOCK] 1 of 1 target completed, 1 valid pair found.\n"
            "[DEMO / MOCK] Hydra audit finished."
        )

        findings = [
            {
                "title": f"[DEMO / MOCK] Weak {service} Service Credentials (Hydra)",
                "severity": "CRITICAL",
                "vulnerability_type": "Weak Service Authentication",
                "target": f"{target}:{port}",
                "details": f"Simulated Audit Result: Target network service {service} accepted default credential pair 'admin:Password123!'.",
                "remediation": f"Immediately disable root/admin password logins on {service} port {port} and enforce SSH keys / MFA.",
            }
        ]
        return mock_output, findings

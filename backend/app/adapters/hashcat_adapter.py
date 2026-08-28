from typing import List, Dict, Any, Tuple
from app.adapters.base import BaseEngineAdapter


class HashcatAdapter(BaseEngineAdapter):
    """Hashcat Password Auditing Engine Adapter."""

    def __init__(self):
        super().__init__(name="Hashcat", category="Password Audit", requires_network=False)

    def build_command(self, target: str, parameters: Dict[str, Any]) -> List[str]:
        hash_type = str(parameters.get("hash_type", "0"))  # 0 = MD5
        wordlist = str(parameters.get("wordlist", "/usr/share/wordlists/rockyou.txt"))
        rules = parameters.get("rules", None)

        cmd = ["hashcat", "-m", hash_type, "-a", "0", target, wordlist]
        if rules:
            cmd.extend(["-r", str(rules)])
        cmd.append("--quiet")
        return cmd

    def parse_output(self, raw_output: str) -> List[Dict[str, Any]]:
        findings = []
        for line in raw_output.strip().splitlines():
            if ":" in line and not line.startswith("["):
                parts = line.split(":", 1)
                findings.append({
                    "title": "Weak Password Identified (Hashcat)",
                    "severity": "HIGH",
                    "vulnerability_type": "Weak Password Policy",
                    "target": parts[0],
                    "details": f"Hash cracked successfully. Plaintext password revealed: '{parts[1]}'",
                    "remediation": "Enforce strong password complexity policy and multi-factor authentication (MFA)."
                })
        return findings

    def generate_mock_results(self, target: str, parameters: Dict[str, Any]) -> Tuple[str, List[Dict[str, Any]]]:
        mock_output = (
            "[DEMO / MOCK] Hashcat v6.2.6 initialized in simulation mode.\n"
            "[DEMO / MOCK] Dictionary attack against target hash: " + target + "\n"
            "[DEMO / MOCK] Cracked 1 hash out of 1 in 0.04 seconds.\n"
            f"{target}:Admin2026!\n"
            "[DEMO / MOCK] Hashcat audit complete."
        )

        findings = [
            {
                "title": "[DEMO / MOCK] Weak Password Identified (Hashcat)",
                "severity": "HIGH",
                "vulnerability_type": "Weak Password Policy",
                "target": target,
                "details": "Simulated Audit Result: Target hash cracked against standard dictionary list. Plaintext credential: 'Admin2026!'.",
                "remediation": "Enforce mandatory 16+ character passphrase requirements and block common password list hits."
            }
        ]
        return mock_output, findings

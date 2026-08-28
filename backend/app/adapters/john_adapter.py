from typing import List, Dict, Any, Tuple
from app.adapters.base import BaseEngineAdapter


class JohnAdapter(BaseEngineAdapter):
    """John the Ripper Password Auditing Engine Adapter."""

    def __init__(self):
        super().__init__(name="John the Ripper", category="Password Audit", requires_network=False)

    def build_command(self, target: str, parameters: Dict[str, Any]) -> List[str]:
        format_flag = parameters.get("format", None)
        wordlist = str(parameters.get("wordlist", "/usr/share/wordlists/rockyou.txt"))

        cmd = ["john", f"--wordlist={wordlist}"]
        if format_flag:
            cmd.append(f"--format={format_flag}")
        cmd.append(target)
        return cmd

    def parse_output(self, raw_output: str) -> List[Dict[str, Any]]:
        findings = []
        for line in raw_output.strip().splitlines():
            if "loaded 1 password hash" in line.lower() or "password hash" in line.lower():
                continue
            if "(" in line and ")" in line:
                findings.append({
                    "title": "Weak Password Cracked (John the Ripper)",
                    "severity": "HIGH",
                    "vulnerability_type": "Weak Password Policy",
                    "target": line.strip(),
                    "details": f"John the Ripper cracked credential: {line.strip()}",
                    "remediation": "Update user credentials and enforce robust password complexity filters."
                })
        return findings

    def generate_mock_results(self, target: str, parameters: Dict[str, Any]) -> Tuple[str, List[Dict[str, Any]]]:
        mock_output = (
            "[DEMO / MOCK] John the Ripper 1.9.0-jumbo-1 initialized.\n"
            "[DEMO / MOCK] Loaded 1 password hash (raw-sha256 [SHA256 256/256 AVX2 8x]).\n"
            "[DEMO / MOCK] Press 'q' or Ctrl-C to abort, 'h' for help.\n"
            "password123        (user_admin)\n"
            "[DEMO / MOCK] 1g 0:00:00:01 DONE (2026-08-28 21:50) 1.000g/s 400.0p/s 400.0c/s 400.0C/s password123\n"
            "[DEMO / MOCK] Session completed."
        )

        findings = [
            {
                "title": "[DEMO / MOCK] Weak Credential Recovered (John the Ripper)",
                "severity": "HIGH",
                "vulnerability_type": "Weak Password Policy",
                "target": target,
                "details": "Simulated Audit Result: Hash cracked via dictionary ruleset. Recovered plaintext: 'password123' for user_admin.",
                "remediation": "Rotate compromised account credentials and mandate password manager usage."
            }
        ]
        return mock_output, findings

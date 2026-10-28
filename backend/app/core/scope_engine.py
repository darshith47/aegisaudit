import ipaddress
from typing import Optional, Tuple

from app.models.scope import Scope


class ScopeEngine:
    """Centralized Target Scope & Network Policy Validation Engine.

    Ensures no network security engine or assessment task can execute against
    unauthorized hosts, IP addresses, subnets, ports, or network protocols.
    """

    @staticmethod
    def validate_target(
        scope: Scope, target: str, port: Optional[int] = None, protocol: Optional[str] = None
    ) -> Tuple[bool, str]:
        """Validate if a given target host/IP/hash and optional port/protocol are in-scope."""
        if not target or not target.strip():
            return False, "Target string cannot be empty."

        clean_target = target.strip().lower()

        # Handle offline hash targets (Hashcat / John)
        if ScopeEngine._is_hash_target(clean_target):
            return (
                True,
                "Offline hash target automatically permitted within authorized scope policy.",
            )

        # Extract host if target includes port (e.g. 192.168.1.10:22)
        if ":" in clean_target and not clean_target.startswith("[") and "/" not in clean_target:
            parts = clean_target.split(":")
            if len(parts) == 2 and parts[1].isdigit():
                clean_target = parts[0]
                if port is None:
                    port = int(parts[1])

        # Parse allowed target rules from Scope model
        allowed_rules = [r.strip().lower() for r in scope.allowed_targets.split(",") if r.strip()]
        if not allowed_rules:
            return False, "Scope policy contains no allowed targets."

        # Check target host against scope rules
        host_permitted = False
        match_reason = ""

        try:
            target_ip = ipaddress.ip_address(clean_target)
            for rule in allowed_rules:
                if "/" in rule:
                    try:
                        net = ipaddress.ip_network(rule, strict=False)
                        if target_ip in net:
                            host_permitted = True
                            match_reason = (
                                f"Target IP {clean_target} matches authorized subnet {rule}"
                            )
                            break
                    except ValueError:
                        continue
                else:
                    try:
                        rule_ip = ipaddress.ip_address(rule)
                        if target_ip == rule_ip:
                            host_permitted = True
                            match_reason = f"Target IP {clean_target} matches authorized IP {rule}"
                            break
                    except ValueError:
                        continue
        except ValueError:
            # Target is a domain name
            for rule in allowed_rules:
                if clean_target == rule or clean_target.endswith("." + rule):
                    host_permitted = True
                    match_reason = (
                        f"Target domain {clean_target} matches authorized scope rule {rule}"
                    )
                    break

        if not host_permitted:
            return (
                False,
                f"Target '{target}' is OUT-OF-SCOPE according to Scope policy #{scope.id} ({scope.name}).",
            )

        # Check port authorization if specified
        if port is not None:
            allowed_ports = [p.strip() for p in scope.allowed_ports.split(",") if p.strip()]
            if str(port) not in allowed_ports and "*" not in allowed_ports:
                return (
                    False,
                    f"Port {port} is not in authorized ports allowlist ({scope.allowed_ports}) for Scope #{scope.id}.",
                )

        # Check protocol authorization if specified
        if protocol is not None:
            clean_proto = protocol.strip().lower()
            allowed_protocols = [
                pr.strip().lower() for pr in scope.allowed_protocols.split(",") if pr.strip()
            ]
            if clean_proto not in allowed_protocols and "*" not in allowed_protocols:
                return (
                    False,
                    f"Protocol '{protocol}' is not in authorized protocol allowlist ({scope.allowed_protocols}) for Scope #{scope.id}.",
                )

        return True, f"Target authorized: {match_reason}"

    @staticmethod
    def _is_hash_target(target: str) -> bool:
        """Check if target string represents a cryptographic hash or hash file representation."""
        # Simple heuristic for common hashes (MD5, SHA1, SHA256, bcrypt, NTLM)
        if target.startswith(("$2a$", "$2b$", "$2y$", "$6$", "$5$")):
            return True
        if len(target) in (32, 40, 64) and all(c in "0123456789abcdefABCDEF" for c in target):
            return True
        if (
            target.endswith(".hash")
            or target.endswith(".txt")
            or ":" in target
            and len(target.split(":")[0]) in (32, 40)
        ):
            return True
        return False

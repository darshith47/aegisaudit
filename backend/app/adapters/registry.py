from typing import Any, Dict, List, Optional

from app.adapters.base import BaseEngineAdapter
from app.adapters.hashcat_adapter import HashcatAdapter
from app.adapters.hydra_adapter import HydraAdapter
from app.adapters.john_adapter import JohnAdapter


class EngineRegistry:
    """Centralized Security Engine Registry & Engine Matrix Provider."""

    def __init__(self) -> None:
        self._adapters: Dict[str, BaseEngineAdapter] = {
            "hashcat": HashcatAdapter(),
            "john": JohnAdapter(),
            "hydra": HydraAdapter(),
        }

    def get_adapter(self, engine_name: str) -> Optional[BaseEngineAdapter]:
        """Get implementation adapter for supported engine name."""
        return self._adapters.get(engine_name.lower())

    def get_engine_matrix(self) -> List[Dict[str, Any]]:
        """Return full Engine Matrix showing Implemented vs Planned engines."""
        matrix = [
            {
                "engine": "Hashcat",
                "category": "Password Audit",
                "status": "Implemented",
                "network": "No",
                "scope": "N/A",
            },
            {
                "engine": "John",
                "category": "Password Audit",
                "status": "Implemented",
                "network": "No",
                "scope": "N/A",
            },
            {
                "engine": "Hydra",
                "category": "Authentication",
                "status": "Implemented",
                "network": "Yes",
                "scope": "Required",
            },
            {
                "engine": "Medusa",
                "category": "Authentication",
                "status": "Planned",
                "network": "Yes",
                "scope": "Required",
            },
            {
                "engine": "Ncrack",
                "category": "Authentication",
                "status": "Planned",
                "network": "Yes",
                "scope": "Required",
            },
            {
                "engine": "CeWL",
                "category": "Wordlist",
                "status": "Planned",
                "network": "Yes",
                "scope": "Required",
            },
            {
                "engine": "Crunch",
                "category": "Wordlist",
                "status": "Planned",
                "network": "No",
                "scope": "N/A",
            },
            {
                "engine": "Pack",
                "category": "Analysis",
                "status": "Planned",
                "network": "No",
                "scope": "N/A",
            },
            {
                "engine": "Mentalist",
                "category": "Wordlist",
                "status": "Planned",
                "network": "No",
                "scope": "N/A",
            },
            {
                "engine": "Hashid",
                "category": "Identification",
                "status": "Planned",
                "network": "No",
                "scope": "N/A",
            },
            {
                "engine": "Nmap",
                "category": "Scope Verification",
                "status": "Planned",
                "network": "Yes",
                "scope": "Required",
            },
        ]
        return matrix


engine_registry = EngineRegistry()

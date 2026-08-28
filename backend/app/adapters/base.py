from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any, List
from app.models.scope import Scope
from app.core.scope_engine import ScopeEngine


class BaseEngineAdapter(ABC):
    """Abstract Base Class for Security Engine Adapters."""

    def __init__(self, name: str, category: str, requires_network: bool = False):
        self.name = name
        self.category = category
        self.requires_network = requires_network

    def validate_scope(self, scope: Scope, target: str, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate if the engine operation against the target is within authorized scope."""
        port = parameters.get("port")
        protocol = parameters.get("protocol") or parameters.get("service")
        return ScopeEngine.validate_target(scope=scope, target=target, port=port, protocol=protocol)

    @abstractmethod
    def build_command(self, target: str, parameters: Dict[str, Any]) -> List[str]:
        """Construct safe command-line arguments list (never a raw shell string)."""
        pass

    @abstractmethod
    def parse_output(self, raw_output: str) -> List[Dict[str, Any]]:
        """Parse raw security tool output into structured findings."""
        pass

    @abstractmethod
    def generate_mock_results(self, target: str, parameters: Dict[str, Any]) -> Tuple[str, List[Dict[str, Any]]]:
        """Generate safe, synthetic mock results clearly tagged with DEMO / MOCK."""
        pass

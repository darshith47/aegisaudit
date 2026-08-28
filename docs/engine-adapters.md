# AegisAudit — Security Engine Adapters Specification

## Overview

AegisAudit utilizes a modular engine-adapter model. Security tools (password auditors, network authentication testers, wordlist generators) are wrapped in typed Python adapter classes inheriting from `BaseEngineAdapter`.

---

## Adapter Interface Contract

Every adapter must implement:

```python
class BaseEngineAdapter(ABC):
    def validate_scope(self, scope: Scope, target: str, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        ...

    @abstractmethod
    def build_command(self, target: str, parameters: Dict[str, Any]) -> List[str]:
        ...

    @abstractmethod
    def parse_output(self, raw_output: str) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def generate_mock_results(self, target: str, parameters: Dict[str, Any]) -> Tuple[str, List[Dict[str, Any]]]:
        ...
```

---

## Adding a New Security Adapter

To add a new security engine adapter (e.g. Medusa):

1. Create `app/adapters/medusa_adapter.py` subclassing `BaseEngineAdapter`.
2. Implement `build_command()`, `parse_output()`, and `generate_mock_results()`.
3. Register the new adapter instance in `app/adapters/registry.py`.
4. Update the Engine Matrix table in `README.md` and `registry.py`.

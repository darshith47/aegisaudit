from app.adapters.hashcat_adapter import HashcatAdapter
from app.adapters.hydra_adapter import HydraAdapter
from app.adapters.john_adapter import JohnAdapter
from app.adapters.registry import engine_registry


def test_engine_registry_matrix():
    matrix = engine_registry.get_engine_matrix()
    assert len(matrix) >= 10
    hashcat_entry = next(e for e in matrix if e["engine"] == "Hashcat")
    assert hashcat_entry["status"] == "Implemented"
    medusa_entry = next(e for e in matrix if e["engine"] == "Medusa")
    assert medusa_entry["status"] == "Planned"


def test_hashcat_adapter_mock_mode():
    adapter = HashcatAdapter()
    target = "5f4dcc3b5aa765d61d8327deb882cf99"
    output, findings = adapter.generate_mock_results(target, {})
    assert "[DEMO / MOCK]" in output
    assert len(findings) == 1
    assert findings[0]["severity"] == "HIGH"


def test_john_adapter_mock_mode():
    adapter = JohnAdapter()
    target = "user_admin:password123"
    output, findings = adapter.generate_mock_results(target, {})
    assert "[DEMO / MOCK]" in output
    assert len(findings) == 1
    assert findings[0]["severity"] == "HIGH"


def test_hydra_adapter_command_building():
    adapter = HydraAdapter()
    cmd = adapter.build_command("10.0.0.5", {"username": "admin", "service": "ssh", "port": 22})
    assert "hydra" in cmd
    assert "-l" in cmd
    assert "admin" in cmd
    assert "10.0.0.5" in cmd
    assert "ssh" in cmd

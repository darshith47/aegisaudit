from app.core.scope_engine import ScopeEngine


def test_scope_engine_in_scope_ip(test_scope):
    allowed, reason = ScopeEngine.validate_target(test_scope, "10.0.0.45", port=22, protocol="ssh")
    assert allowed is True
    assert "matches authorized subnet" in reason


def test_scope_engine_out_of_scope_ip(test_scope):
    allowed, reason = ScopeEngine.validate_target(test_scope, "8.8.8.8", port=22, protocol="ssh")
    assert allowed is False
    assert "OUT-OF-SCOPE" in reason


def test_scope_engine_unauthorized_port(test_scope):
    allowed, reason = ScopeEngine.validate_target(
        test_scope, "10.0.0.45", port=8443, protocol="https"
    )
    assert allowed is False
    assert "Port 8443 is not in authorized ports allowlist" in reason


def test_scope_api_validation(client, auth_headers, test_scope):
    res = client.post(
        "/api/v1/scope/validate",
        headers=auth_headers,
        json={"scope_id": test_scope.id, "target": "10.0.0.50", "port": 80, "protocol": "http"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["is_allowed"] is True

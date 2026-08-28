def test_assessment_and_job_execution(client, auth_headers, test_scope):
    # 1. Create Assessment with In-Scope target
    ass_res = client.post(
        "/api/v1/assessments/",
        headers=auth_headers,
        json={
            "title": "Lab SSH Credential Audit",
            "description": "Authorized audit against internal lab server",
            "target": "10.0.0.15",
            "engine": "hydra",
            "scope_id": test_scope.id
        }
    )
    assert ass_res.status_code == 201
    assessment_id = ass_res.json()["id"]

    # 2. Launch Job
    job_res = client.post(
        "/api/v1/jobs/launch",
        headers=auth_headers,
        json={"assessment_id": assessment_id, "parameters": {"username": "admin", "service": "ssh", "port": 22}}
    )
    assert job_res.status_code == 201
    job_data = job_res.json()
    assert job_data["status"] == "completed"
    assert "[DEMO / MOCK]" in job_data["output"]


def test_job_rejection_out_of_scope(client, auth_headers, test_scope):
    # Create Assessment with OUT-OF-SCOPE target
    ass_res = client.post(
        "/api/v1/assessments/",
        headers=auth_headers,
        json={
            "title": "Unauthorized External Scan Attempt",
            "target": "8.8.8.8",
            "engine": "hydra",
            "scope_id": test_scope.id
        }
    )
    assert ass_res.status_code == 201
    assessment_id = ass_res.json()["id"]

    # Launch Job -> Scope Engine MUST Reject
    job_res = client.post(
        "/api/v1/jobs/launch",
        headers=auth_headers,
        json={"assessment_id": assessment_id, "parameters": {"username": "admin", "service": "ssh"}}
    )
    assert job_res.status_code == 201
    job_data = job_res.json()
    assert job_data["status"] == "rejected_out_of_scope"
    assert "REJECTED BY CENTRALIZED SCOPE ENGINE" in job_data["output"]

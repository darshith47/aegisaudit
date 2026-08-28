def test_report_generation(client, auth_headers, test_scope):
    # Setup assessment & job
    ass_res = client.post(
        "/api/v1/assessments/",
        headers=auth_headers,
        json={"title": "Report Test Assessment", "target": "10.0.0.20", "engine": "hashcat", "scope_id": test_scope.id}
    )
    assessment_id = ass_res.json()["id"]

    client.post(
        "/api/v1/jobs/launch",
        headers=auth_headers,
        json={"assessment_id": assessment_id, "parameters": {}}
    )

    # Test Markdown report generation
    rep_res = client.post(
        "/api/v1/reports/generate",
        headers=auth_headers,
        json={"assessment_id": assessment_id, "format": "markdown"}
    )
    assert rep_res.status_code == 200
    report_data = rep_res.json()
    assert "AegisAudit" in report_data["content"]
    assert "Executive Report" in report_data["content"]

    # Test HTML report view
    html_res = client.get(
        f"/api/v1/reports/{assessment_id}/html",
        headers=auth_headers
    )
    assert html_res.status_code == 200
    assert "<!DOCTYPE html>" in html_res.text

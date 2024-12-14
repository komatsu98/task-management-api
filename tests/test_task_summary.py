from fastapi import status


# Test employee task summary pagination endpoint
def test_employee_task_summary_pagination(client, get_auth_token_employer):
    token = get_auth_token_employer
    response = client.get(
        "/api/v1/employees/tasks-summary?page=1&limit=5",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "data" in data
    assert "metadata" in data
    assert len(data["data"]) >= 1
    assert len(data["data"]) <= 5

    summary = data["data"][0]
    assert "employee_id" in summary
    assert "username" in summary
    assert "total_tasks_assigned" in summary
    assert "completed_tasks" in summary

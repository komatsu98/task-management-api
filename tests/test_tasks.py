from fastapi import status


# Test creating a task
def test_create_task(client, get_auth_token_employer):
    token = get_auth_token_employer
    task_data = {
        "title": "Complete project documentation",
        "due_date": "2024-12-31",
        "assignee_id": 1,
    }
    response = client.post(
        "/api/v1/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "title" in response.json()


# Test filtering tasks with pagination and sorting
def test_filter_tasks_pagination(client, get_auth_token_employee):
    token = get_auth_token_employee

    response = client.get(
        "/api/v1/tasks?status=pending&page=1&limit=10",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    tasks_data = response.json().get("data")

    assert tasks_data is not None
    assert len(tasks_data) <= 10


# Test updating a task
def test_update_task(client, get_auth_token_employee):
    token = get_auth_token_employee
    task_update_data = {"status": "completed"}

    response = client.put(
        "/api/v1/tasks/1",
        json=task_update_data,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    updated_task = response.json()

    assert updated_task["status"] == "completed"


# Test deleting a task
def test_delete_task(client, get_auth_token_employer):
    token = get_auth_token_employer

    response = client.delete(
        "/api/v1/tasks/1", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

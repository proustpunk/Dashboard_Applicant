from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_create_candidate():

    response = client.post(
        "/candidates",
        json={
            "name": "Test Candidate",
            "email": "testcandidate4@example.com",
            "role_applied": "Backend Engineer",
            "skills": ["Python", "FastAPI"]
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200


from app.routers.auth import create_access_token


def get_auth_header(email):
    token = create_access_token(
        {
            "sub": email,
            "role": "REVIEWER"
        }
    )

    return {
        "Authorization": f"Bearer {token}"
    }


def test_reviewer_cannot_see_other_reviewers_scores():

    candidate_response = client.post(
        "/candidates",
        json={
            "name": "Candidate Test",
            "email": "candidate4@test.com",
            "role_applied": "Backend",
            "skills": ["Python"]
        }
    )

    candidate_id = candidate_response.json()["id"]


    # reviewer A creates score
    client.post(
        f"/candidates/{candidate_id}/scores",
        headers=get_auth_header("reviewer1@test.com"),
        json={
            "category": "Python",
            "score": 5,
            "note": "Good"
        }
    )


    # reviewer B fetches candidate
    response = client.get(
        f"/candidates/{candidate_id}",
        headers=get_auth_header("reviewer2@test.com")
    )


    data = response.json()

    print(data)
    assert len(data["scores"]) == 0
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from Routes.AdminRoutes import admin_router
from Database.db import get_db as admin_get_db
from Routes.ResearcherRoutes import researcher_router
from Database.db import get_db as researcher_get_db


def _admin_client(mock_db):
    app = FastAPI()
    app.include_router(admin_router, prefix="/api")
    app.dependency_overrides[admin_get_db] = lambda: mock_db
    return TestClient(app)


def _researcher_client(mock_db):
    app = FastAPI()
    app.include_router(researcher_router, prefix="/api")
    app.dependency_overrides[researcher_get_db] = lambda: mock_db
    return TestClient(app)


def test_admin_delete_user_incorrectly_rejects_admin_role_bug(monkeypatch):

    monkeypatch.setattr(
        "Routes.AdminRoutes.RBAC",
        lambda request, db: {"role": "Admins", "user_id": "admin-id"},
    )
    mock_db = MagicMock()
    client = _admin_client(mock_db)

    response = client.post(
        "/api/admin_routes/delete_user",
        json={"username": "bob", "usernameconfirm": "bob"},
    )

    assert response.status_code == 403


def test_choose_recommender_crashes_on_valid_selection_due_to_datetime_shadowing_bug(monkeypatch):

    monkeypatch.setattr(
        "Routes.ResearcherRoutes.RBAC",
        lambda request, db: {"role": "Researchers", "user_id": "researcher-id"},
    )
    mock_db = MagicMock()
    mock_db.execute.return_value.scalar_one_or_none.return_value = None
    client = _researcher_client(mock_db)

    # RContentBasedFiltering.py genuinely exists under RECSYS_V2_RECOMMENDER/
    # in this repo, so the route's real os.listdir() folder scan finds it
    # without needing to mock the filesystem - the crash below happens
    # after that check passes, not because of it.
    with pytest.raises(AttributeError):
        client.post(
            "/api/researcher_routes/choose_recommender_algorithm",
            json={"algorithm_name": "RContentBasedFiltering"},
        )

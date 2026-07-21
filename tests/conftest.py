from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


ORIGINAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture
def client():
    """Return a test client with a reset in-memory activities state."""
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))

    return TestClient(app)

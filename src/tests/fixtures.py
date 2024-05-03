import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        username="test", email="test@example.com", password="secret"
    )

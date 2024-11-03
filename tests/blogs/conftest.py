import pytest


@pytest.fixture
def post_data():
    return {
        "title": "Test Title",
        "content": "This is test content.",

    }

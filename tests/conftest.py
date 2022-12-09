import pytest 

from project import create_app

@pytest.fixture(scope='function')
def test_client():
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='function')
def reset(test_client):
    test_client.delete("/reset_table")
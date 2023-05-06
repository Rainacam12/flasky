import pytest
# import create app to use the function to create an instance 
from app import create_app
# import db bc we make an instance of the db we will be working with on line 14
from app import db
# import request_finished to avoid working with old cached data. we want the most recent to avoid false positives 
from flask.signals import request_finished
from app.models.crystal import Crystal


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()


    with app.app_context():
        db.create_all()
        yield app

    # after the test is finished with the logic that was passed into it, we will drop all tables 
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def make_two_crystals(app):
    crystal_1 = Crystal(
        name="pearl",
        color="white",
        powers="pretty powers"
    )

    crystal_2 = Crystal(
        name="Garnet",
        color="Red",
        powers="Awesomeness"
    )

    db.session.add_all([crystal_1, crystal_2])
    db.session.commit()
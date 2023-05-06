from flask import Flask
# 4/28 import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# import Migrate 
from flask_migrate import Migrate
# import library for  dotenv to grab env vars
from dotenv import load_dotenv 
# read env vars 
import os

# give us access to db ops
db = SQLAlchemy()
migrate = Migrate()
# load the values from .env file to os module so that it can read the values 
load_dotenv()

def create_app(test_config=None):
    # __name__ stores the name of the module we're in
    app = Flask(__name__)
    
    # set up the database
    if not test_config:
        # dev environment configuration
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        # test environment configuration 
        # if there is a test_config passed in, this means we are trying to test the app 
        # configure the test settings 
        app.config["TESTING"] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    # connect the db and migrate to our flask app
    db.init_app(app)
    migrate.init_app(app, db)

    # import routes
    from .routes import crystal_bp
    # register the blueprint
    app.register_blueprint(crystal_bp)
    
    # import so db can see the model
    from app.models.crystal import Crystal
    return app
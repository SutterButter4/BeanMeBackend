# flask packages
# external packages
import os

from flask import Flask, app
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from flask_restful import Api

# local packages
from api.routes import create_routes
from models.user import Users

# default mongodb configuration
default_config = {'MONGODB_SETTINGS': {
                    'db': 'beanme',
                    'host': 'mongodb+srv://admin:TvUPRBOAGTn6lBBL@cluster0.fv5vo.mongodb.net/beanme?retryWrites=true&w=majority',
                    },
                  'JWT_SECRET_KEY': 'changeThisKeyFirst'}



def get_flask_app(config: dict = None) -> app.Flask:
    """
    Initializes Flask app with given configuration.
    Main entry point for wsgi (gunicorn) server.
    :param config: Configuration dictionary
    :return: app
    """
    # init flask
    flask_app = Flask(__name__)

    # configure app
    config = default_config if config is None else config
    flask_app.config.update(config)

    # load config variables
    if 'MONGODB_URI' in os.environ:
        flask_app.config['MONGODB_SETTINGS'] = {'host': os.environ['MONGODB_URI'],
                                                'retryWrites': False}
    if 'JWT_SECRET_KEY' in os.environ:
        flask_app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

    # init api and routes
    api = Api(app=flask_app)
    create_routes(api=api)

    # init mongoengine
    db = MongoEngine(app=flask_app)

    # init jwt manager
    jwt = JWTManager(app=flask_app)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return Users.objects.get(id=identity)

    return flask_app




if __name__ == '__main__':
    # Main entry point when run in stand-alone mode.
    print("v5")

    app = get_flask_app()
    app.run(debug=True, port=80, host="0.0.0.0")


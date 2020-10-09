from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from api_rest.sql_alchemy import db


def create_app(config):
    """
    
    @param config: 
    @return: 
    """ ""
    app = Flask(__name__)
    app.config.from_object(config)
    return app


def initialize_db(app):
    """

    @return:
    """
    db.init_app(app)
    return db


def initialize_api(app):
    """

    @return:
    """
    api = Api(app)
    return api


def initialize_jwt(app):
    """

    @param app:
    @return:
    """
    jwt = JWTManager(app)
    return jwt

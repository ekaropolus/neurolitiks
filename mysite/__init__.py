from flask import Flask
from flask_bcrypt import Bcrypt
from mysite.config import Config

from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi

bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)
    bcrypt.init_app(app)

    from mysite.main.routes import main
    app.register_blueprint(main)

    from mysite.public_policies.routes import public_policies
    app.register_blueprint(public_policies)

    uri = "mongodb+srv://ekaropolus:uauZb56qa8Bdr1I6@neurolitiks.nihgty2.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    app.mongo_policies = client["Neurolitiks"]
    app.mongo_policies.policies.insert_one({})

    return app





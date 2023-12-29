from flask import Flask

from mysite.config import Config, URI_MONGO
from mysite.users.models import User

from pymongo import MongoClient
from pymongo.server_api import ServerApi

from flask_login import LoginManager
login_manager = LoginManager()

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from bson import ObjectId

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)
    

    login_manager.init_app(app)
    
    bcrypt.init_app(app)
    
    # Import and register Blueprints
    from mysite.main.routes import main
    app.register_blueprint(main)
    
    from mysite.public_policies.routes import public_policies
    app.register_blueprint(public_policies)
    
    from mysite.users.routes import users
    app.register_blueprint(users, url_prefix='/users/')
    
    # MongoDB client setup
    client = MongoClient(URI_MONGO, server_api=ServerApi('1'))
    app.mongo_neurolitiks = client["Neurolitiks"]

    # Ensure there is always an admin user
    admin_user = {
        "username": "admin",
        "roles": ["admin"],
        # Add other necessary fields such as oauth_provider, etc.
    }
    # Check if admin user exists, create if not
    if app.mongo_neurolitiks.users.count_documents({"username": "admin"}) == 0:
        app.mongo_neurolitiks.users.insert_one(admin_user)

    @login_manager.user_loader
    def load_user(user_id):
        user_doc = app.mongo_neurolitiks.users.find_one({'_id': ObjectId(user_id)})
        if user_doc:
            return User(user_id=user_doc['_id'], username=user_doc['username'], roles=user_doc['roles'])
        return None

    return app

from flask import current_app
from flask_login import login_manager
from .models import User
from bson import ObjectId

@login_manager.user_loader
def load_user(user_id):
    user_doc = current_app.mongo_neurolitiks.users.find_one({'_id': ObjectId(user_id)})
    if user_doc:
        return User(user_id=user_doc['_id'], username=user_doc['username'], roles=user_doc['roles'])
    return None
import json

from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource

# project resources
from api.response import success
from models.user import Users
from models.notifications import Notifications


class root(Resource):
    def get(self):
        return success()



#return the single user that called this method from the front end
class getUser(Resource):
    @jwt_required()
    def get(self):
        return success(json.loads(current_user.to_json()))


#return the single user that called this method from the front end
class notifications(Resource):
    @jwt_required()
    def post(self):
        Notifications.objects(userOwnerId=current_user.id).update(viewed=True)
        return success(current_user.to_json())

    @jwt_required()
    def get(self):
        user_id = current_user.id
        return success(Notifications.objects(userOwnerId=user_id).to_json())
    
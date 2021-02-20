# flask packages
import json

import jwt
from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from bson.objectid import ObjectId

# project resources
from models.user import Users
from models.group import Groups, GroupUser, ScheduledTask
from models.task import Tasks


from api.errors import not_found_error, unauthorized_error, success

import json

class root(Resource):
    def get(self):
        return "OK", 200



#return the single user that called this method from the front end
class getUser(Resource):
    @jwt_required()
    def post(self):
        return current_user.to_json()





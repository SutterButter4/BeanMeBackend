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


from api.response import not_found_error, unauthorized_error, success

import json

class root(Resource):
    def get(self):
        return "OK", 200



#return the single user that called this method from the front end
class getUser(Resource):
    @jwt_required()
    def post(self):
        return current_user.to_json()


#return the single user that called this method from the front end
class notifcations(Resource):
    @jwt_required()
    def post(self):
        current_user.update("set__notications__viewed"=True)
        return current_user.to_json()



def notifcations(type="",userId=none,groupId=none,taskId=none,amount=0):
    if(userId):
        try:
            username = Users.objects.get(id:userId)
        except:
            return 0
    if(groupId):
        try:
            username = Users.objects.get(id:userId)
        except:
            return 0
    if(taskId):
        try:
            username = Users.objects.get(id:userId)
        except:
            return 0
    if(string=="INVITE"):
        d = f"You've been invited to join {group_name}"
    elif(string=="TASK_CREATED"):
        d = f"{username_of_creator} wants {bean_reward} for {task_description}"
    elif(string=="TASK_FULFILLED"):
        d = f"{group_name} has found {bean_reward} beans for {task_description}"
    elif(string=="OUT_OF_BEANS"):
        d = f"{username} is out of beans"
    elif(string=="INCOMING_TRANSFER"):
        d = f"{username} has given you {amonut} beans"
    elif(string=="USER_JOINED"):
        d = f"{username} has joined {group name}"

    return
    
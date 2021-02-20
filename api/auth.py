# flask packages
from flask import Response, request, jsonify, redirect
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token

# project resources
from models.user import Users
from api.response import unauthorized_error, bad_request_error

# external packages
import datetime


class SignUpApi(Resource):

    @staticmethod
    def post() -> Response:
        """
        POST response method for creating user.
        :return: JSON object
        """
        data = request.get_json()
        try:
            post_user = Users(**data)
            post_user.save()
            return redirect("/auth/login")
        except:
            return bad_request_error("User with these credentials already exists");



class LoginApi(Resource):

    @staticmethod
    def post() -> Response:
        """
        POST response method for retrieving user web token.
        :return: JSON object
        """
        data = request.get_json()
        user = Users.objects.get(name=data.get('name'))
        auth_success = user.check_pw_hash(data.get('password'))
        if not auth_success:
            return unauthorized_error("failed to login");
        else:
            expiry = datetime.timedelta(days=5)
            access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
            refresh_token = create_refresh_token(identity=str(user.id))
            return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
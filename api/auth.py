# flask packages
# external packages
import datetime
import json

from flask import Response, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource

from api.response import unauthorized_error, bad_request_error
# project resources
from models.user import Users


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
        except Exception as e:
            return bad_request_error(str(e))

        expiry = datetime.timedelta(days=5)
        access_token = create_access_token(identity=str(post_user.id), expires_delta=expiry)
        refresh_token = create_refresh_token(identity=str(post_user.id))
        return jsonify({'access_token': access_token, 'refresh_token': refresh_token, 'user': json.loads(post_user.to_json())})

class LoginApi(Resource):

    @staticmethod
    def post() -> Response:
        """
        POST response method for retrieving user web token.
        :return: JSON object
        """
        data = request.get_json()

        try:
            user = Users.objects.get(phone=data.get('phone'))
        except:
            return bad_request_error("user with phone# not found")

        auth_success = user.check_pw_hash(data.get('password'))
        if not auth_success:
            return unauthorized_error("failed to login")
        else:
            expiry = datetime.timedelta(days=5)
            access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
            refresh_token = create_refresh_token(identity=str(user.id))
            return jsonify({'access_token': access_token, 'refresh_token': refresh_token, 'user': json.loads(user.to_json())})
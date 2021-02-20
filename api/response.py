from flask import Response, jsonify


def bad_request_error(msg) -> Response:
    resp = jsonify({"error":msg})
    resp.status_code = 400
    return resp

def unauthorized_error(msg) -> Response:
    resp = jsonify({"error":msg})
    resp.status_code = 401
    return resp


def not_found_error(msg) -> Response:
    resp = jsonify({"error":msg})
    resp.status_code = 404
    return resp

def success(data="OK") -> Response:
    resp = jsonify(data)
    resp.status_code = 201
    return resp
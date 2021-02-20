from flask import Response, jsonify


def bad_request_error(msg) -> Response:
    output = {"error":
              {"msg": "403 error: %s" % msg}
              }
    resp = jsonify({'result': output})
    resp.status_code = 403
    return resp

def unauthorized_error(msg) -> Response:
    output = {"error":
              {"msg": "401 error: %s" % msg}
              }
    resp = jsonify({'result': output})
    resp.status_code = 401
    return resp


def not_found_error(msg) -> Response:
    output = {"error":
              {"msg": "404 error: %s" % msg}
              }
    resp = jsonify({'result': output})
    resp.status_code = 404
    return resp
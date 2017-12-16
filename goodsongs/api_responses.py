"""API response helpers."""

from flask import jsonify


def ok(data=None):
    """Create an OK HTTP response with the given data."""
    data = data if data else {}
    if 'data' not in data:
        data = {'data': data}
    response = jsonify(data)
    response.status_code = 200
    return response


def unprocessable_entity(message=None):
    """Create an Unprocessable Entity HTTP response with the given message."""
    return create_error_response(422, message)


def not_found(message=None):
    """Create an Not Found HTTP response with the given message."""
    return create_error_response(404, message)


def create_error_response(status_code, message):
    """Create an error response with the given code and message."""
    data = {}
    if message:
        data = {'error': {'message': message}}
    response = jsonify(data)
    response.status_code = status_code
    return response

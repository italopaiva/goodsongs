"""API response helpers."""

from flask import jsonify


def ok(data=None):
    """Create a HTTP OK response with the given data."""
    return create_success_response(200, data)


def created(data=None):
    """Create a HTTP Created response with the given data."""
    return create_success_response(201, data)


def unprocessable_entity(message=None):
    """Create a HTTP Unprocessable Entity response with the given message."""
    return create_error_response(422, message)


def not_found(message=None):
    """Create a HTTP Not Found response with the given message."""
    return create_error_response(404, message)


def create_error_response(status_code, message):
    """Create an error response with the given status and message."""
    data = {}
    if message:
        data = {'error': {'message': message}}
    response = jsonify(data)
    response.status_code = status_code
    return response


def create_success_response(status_code, data):
    """Create a success response with the given status and message."""
    data = data if data else {}
    if 'data' not in data:
        data = {'data': data}
    response = jsonify(data)
    response.status_code = status_code
    return response

from functools import wraps
from flask import request
from server.controllers.authentication import find_user

def require_login(parser):
    """
    Makes sure certificate is used, and user exists.
    """

    def wrapper(func):
        @wraps(func)
        def inner(self):
            data = parser.parse_args()
            user = find_user(request.environ.get('SSL_CLIENT_S_DN_Email', None))
            if (user is None):
                return return_failure("No such user.")
            value = func(self, data, user)
            return value
        return inner
    return wrapper

def return_failure(message, error_code=500):
    """
        Generates JSON for a failed API request
    """
    return {"success": False, "error": message, "error_code": error_code}


def return_success(data=None):
    """
        Generates JSON for a successful API request
    """
    if data is None:
        return {"success": True}
    return {"success": True, **data}

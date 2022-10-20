from server.models.user import User

def find_user(email):
    """
    Finds the user with the email.
    """
    if email is not None:
        return User.query.filter_by(email=email).first()
    return None

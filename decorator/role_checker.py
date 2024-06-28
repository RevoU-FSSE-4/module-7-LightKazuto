from functools import wraps
from flask_login import current_user


def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if (
                current_user.is_authenticated
                and role == "admin"
                and current_user.role == "admin"
            ):
                return func(*args, **kwargs)
            elif (
                current_user.is_authenticated
                and current_user.role == "admin"
                and role == "user"
            ):
                return func(*args, **kwargs)
            elif (
                current_user.is_authenticated
                and role == "user"
                and current_user.role == "user"
            ):
                return func(*args, **kwargs)
            else:
                return {"message": "Unauthorized"}, 403

        return wrapper

    return decorator

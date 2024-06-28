from functools import wraps
from flask_login import current_user


def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated and current_user.role == role:
                return func(*args, **kwargs)
            else:
                return {"message": "Unauthorized"}, 403
            # Case 2 : Admin has more power than User

        return wrapper

    return decorator

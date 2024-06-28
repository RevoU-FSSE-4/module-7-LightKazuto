from functools import wraps
from flask_login import current_user


def role_required(role):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return {"message": "Login required"}, 401

            if current_user.role != role:
                return {"message": "Unauthorized, insufficient role"}, 403

            # Lanjutkan ke fungsi yang asli
            return func(*args, **kwargs)

        return decorated_view

    return decorator

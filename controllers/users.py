from flask import Blueprint, request

from connectors.mysql_connector import connection
from sqlalchemy.orm import sessionmaker
from model.user import User

from flask_login import login_user, current_user, login_required, logout_user
from flask_jwt_extended import create_access_token
from sqlalchemy.orm.exc import UnmappedInstanceError

from decorator.role_checker import role_required

# from flask_jwt_extended import jwt_required


user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/register", methods=["POST"])
def register_userData():
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        NewUser = User(
            username=request.form["username"],
            email=request.form["email"],
            role=request.form["role"],
        )
        NewUser.set_password(request.form["password"])
        s.add(NewUser)
        s.commit()
    except Exception as e:
        print(e)
        s.rollback()
        return {"message": "Fail to Register New User"}, 500
    return {"message": "Success to Create New User"}, 200


@user_routes.route("/login", methods=["POST"])
def login_userData():
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        email = request.form["email"]
        user = s.query(User).filter(User.email == email).first()

        if user == None:
            return {"message": "User not found"}, 403

        if not user.check_password(request.form["password"]):
            return {"message": "Invalid password"}, 403

        login_user(user)
        session_id = request.cookies.get("session")
        return {"session_id": session_id, "message": "Success to Login user"}, 200
    except Exception as e:
        s.rollback()
        return {"message": "Failed to Login User"}, 500


@user_routes.route("/user/<id>", methods=["DELETE"])

def user_delete(id):
    Session = sessionmaker(connection)
    session = Session()
    session.begin()
    try:
        user = session.query(User).filter(User.id == id).first()
        if user is None:
            return {"message": "User not found"}, 404
        session.delete(user)
        session.commit()
        return {"message": "Success delete user data"}, 200
    except UnmappedInstanceError as e:
        session.rollback()
        print(e)
        return {"message": "Failed to delete user"}, 500
    except Exception as e:
        session.rollback()
        print(e)
        return {"message": "Failed to delete user"}, 500
    finally:
        session.close()


@user_routes.route("/logout", methods=["GET"])
def user_logout():
    logout_user()
    return {"message": "Success logout"}

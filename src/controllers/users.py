from flask import Blueprint, request
from connectors.mysql_connector import connection
from sqlalchemy.orm import sessionmaker
from model.user import User
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_user, login_required, logout_user, current_user
from flask import jsonify, abort


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
@login_required
def user_delete(id):
    try:
        Session = sessionmaker(connection)
        with Session() as s:
            user = s.query(User).filter(User.id == id).first()
            if not user:
                abort(404, description="User not found")

            print(f"Deleting user: {user}")

            s.delete(user)
            s.commit()

            print("User deleted successfully")

            return jsonify({"message": "Success delete user data"}), 200

    except SQLAlchemyError as e:
        print("Failed to delete user")
        return jsonify({"message": "Fail to delete user data"}), 500


@user_routes.route("/logout", methods=["GET"])
def user_logout():
    logout_user()
    return {"message": "Success logout"}


@user_routes.route("/user/<id>", methods=["PUT"])
def product_update(id):
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        user = s.query(User).filter(User.id == id).first()

        user.username = request.form["username"]
        user.email = request.form["email"]
        user.role = request.form["role"]

        s.commit()
    except Exception as e:
        s.rollback()
        return {"message": "Fail to Update"}, 500

    return {"message": "Success update product data"}, 200

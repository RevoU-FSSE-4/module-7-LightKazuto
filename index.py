from flask import Flask
from dotenv import load_dotenv
from connectors.mysql_connector import connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, select
from model.user import User
from controllers.users import user_routes
import os
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.register_blueprint(user_routes)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    Session = sessionmaker(connection)
    s =Session()
    return s.query(User).get(user_id)


@app.route("/")
def welcome_web():

#     Session = sessionmaker(connection)
#     with Session() as s:
#         s.execute(
#             text(
#                 "INSERT INTO users (username, email, role_user, password)VALUES('ilham', 'sidiq', 'admin', '12345678')"
#             )
#         )
#         s.commit()

    # Get all data
    user_query = select(User)
    Session = sessionmaker(connection)
    with Session() as s:
        result = s.execute(user_query)
        for row in result.scalars():
            print(f"ID: {row.id}, Name: {row.username}, Role: {row.role}")

    return "Welcome to web user"

from flask import Flask
from dotenv import load_dotenv
from connectors.mysql_connector import connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from model.user import User
from model.review import Review
from controllers.users import user_routes
from controllers.reviews import review_routes
import os
from flask_login import LoginManager
from datetime import timedelta
from flasgger import Swagger


load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=5)
swagger = Swagger(app)


app.register_blueprint(user_routes)
app.register_blueprint(review_routes)

login_manager = LoginManager() 
login_manager.init_app(app)

Session = sessionmaker(connection)

@login_manager.user_loader
def load_user(user_id):
    try:
        with Session() as s:
            return s.query(User).get(user_id)
    except Exception as e:
        print(f"Failed to load user {user_id}: {str(e)}")
        return None


@app.route("/")
def welcome_web():
    return "Welcome to web user"

@app.route("/getData")
def get_dataTerminal():
    user_query = select(User)
    Session = sessionmaker(connection)
    with Session() as s:
        result = s.execute(user_query)
        for row in result.scalars():
            print(f"ID: {row.id}, Name: {row.username}, Role: {row.role}")
    return "Success print data on terminal"

if __name__ == "__main__":
    app.run(debug=True)

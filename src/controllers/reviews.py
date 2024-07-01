from flask import Blueprint, request
from sqlalchemy import select
from connectors.mysql_connector import connection
from sqlalchemy.orm import sessionmaker
from model.review import Review
from sqlalchemy.exc import SQLAlchemyError
from flask_login import current_user
from flask import jsonify


review_routes = Blueprint("riview_routes", __name__)


@review_routes.route("/review_register", methods=["POST"])
def create_review():
    Session = sessionmaker(connection)
    s = Session()
    s.begin()
    try:
        new_review = Review(
            users_id=request.form["users_id"],
            email=request.form["email"],
            rating=request.form["rating"],
            review_content=request.form["review_content"],
        )
        s.add(new_review)
        s.commit()
    except SQLAlchemyError as e:
        s.rollback()
        return jsonify({"error": str(e)}), 400
    return jsonify({"message": "Review berhasil ditambahkan"}), 200


@review_routes.route("/review", methods=["GET"])
def review_all_rating():
    Session = sessionmaker(connection)
    with Session() as s:
        try:
            review_query = select(Review)

            search_keyword = request.args.get("query")
            if search_keyword is not None:
                review_query = review_query.where(
                    Review.review_content.like(f"%{search_keyword}%")
                )

            result = s.execute(review_query)
            reviews = []

            for row in result.scalars():
                reviews.append(
                    {
                        "id": row.id,
                        "email": row.email,
                        "rating": row.rating,
                        "review_content": row.review_content,
                    }
                )

            return {"reviews": reviews, "message": "Hello, " + current_user.email}, 200

        except Exception as e:
            print(e)
            return {"message": "Unexpected Error"}, 500

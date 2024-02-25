import hashlib
import json
import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

load_dotenv()
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
app.config["SECRET_KEY"] = os.getenv("KEY")


def my_get_token(raw_words: str) -> str:
    """
    Gives 64-bit long token for a word
    """
    words = [word.strip('.').lower() for word in raw_words.split()]
    result = [hashlib.sha256(word.encode()).hexdigest() for word in words]
    final_result = ''.join(result)
    hashed_name = hashlib.sha256(final_result.encode()).hexdigest()
    return hashed_name


class Tokens(db.Model):
    book_id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=True, nullable=False)


class Books(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    author: Mapped[str] = mapped_column(unique=False, nullable=False)
    description: Mapped[str] = mapped_column(unique=False, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/tokenize", methods=["POST", "GET"])
def tokenize():
    if request.method == "POST":
        curr_book = request.form.get("title")
        book = db.session.execute(db.select(Books).where(Books.title == curr_book)).scalar()
        if book:
            book_token = db.session.execute(db.select(Tokens).where(Tokens.book_id == book.id)).scalar()
            return render_template("tokenize.html", book_token=book_token)
        else:
            # Book not found
            return render_template("error.html", message="Book not found")

    return render_template("tokenize.html")


@app.route("/detokenize", methods=["POST", "GET"])
def detokenize():
    if request.method == "POST":
        book_token = request.form.get("token")
        table_token = db.session.execute(db.select(Tokens).where(Tokens.token == book_token)).scalar()
        if table_token:
            book = db.session.execute(db.select(Books).where(Books.id == table_token.book_id)).scalar()
            return render_template("detokenize.html", book=book)
        else:
            # Token not found
            return render_template("error.html", message="Token not found")
    return render_template("detokenize.html")


@app.route("/add-data", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        book_title = request.form["title"]
        token_value = my_get_token(book_title.lower())
        token = Tokens(token=token_value)
        db.session.add(token)
        db.session.commit()
        book = Books(
            title=book_title,
            author=request.form["author"],
            description=request.form["description"],
        )
        db.session.add(book)
        db.session.commit()
        return render_template("add.html", book=book, token=token)
    return render_template("add.html")


@app.route("/api/detokenize", methods=["POST"])
def api_detokenize():
    if request.method == "POST":
        json_request = json.loads(request.json)
        book_data = {}

        for key, value in json_request["data"].items():
            # Check for token availability
            token_available = db.session.execute(db.select(Tokens).where(Tokens.token == value)).scalar()

            if token_available:
                # Fetch book details from the database
                details = db.session.execute(db.select(Books).where(Books.id == token_available.book_id)).scalar()
                book_detail = {
                    details.title: {
                        "Author": details.author,
                        "Description": details.description
                    }
                }
                curr_detail = {
                    "found": True,
                    "value": book_detail
                }
                book_data[details.title] = curr_detail
            else:
                curr_detail = {
                    "found": False,
                    "value": ""
                }
                book_data[key] = curr_detail

        response = {
            "user_id": json_request["user_id"],
            "data": book_data
        }
        return jsonify(response)

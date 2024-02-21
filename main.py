from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from flask_bootstrap import Bootstrap5
import hashlib

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
bootstrap = Bootstrap5(app)
app.config["SECRET_KEY"] = "FLASK_KEY"


def my_get_token(raw_words: str) -> str:
    words = [word.strip('.').lower() for word in raw_words.split()]
    result = [hashlib.sha256(word.encode()).hexdigest() for word in words]
    final_result = ''.join(result)
    hashed_name = hashlib.sha256(final_result.encode()).hexdigest()
    return hashed_name


class Tokens(db.Model):
    book_id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=True)


class Books(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str] = mapped_column(unique=False)
    description: Mapped[str] = mapped_column(unique=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/tokenize", methods=["POST", "GET"])
def tokenize():
    if request.method == "POST":
        curr_book = request.form.get("title").lower()
        book = db.session.execute(db.select(Books).where(Books.title == curr_book)).scalar()
        book_token = db.session.execute(db.select(Tokens).where(Tokens.book_id == book.id)).scalar()
        return render_template("result.html", title=curr_book, book_token=book_token)

    return render_template("tokenize.html")


@app.route("/detokenize", methods=["POST", "GET"])
def detokenize():
    if request.method == "POST":
        book_token = request.form.get("token")
        table_token = db.session.execute(db.select(Tokens).where(Tokens.token == book_token)).scalar()
        book = db.session.execute(db.select(Books).where(Books.id == table_token.book_id)).scalar()
        return render_template("book_details.html", book=book)
    return render_template("detokenize.html")


@app.route("/add-data", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        book_title = request.form["title"].lower()
        token_value = my_get_token(book_title)
        token = Tokens(
            token=token_value
        )
        db.session.add(token)
        db.session.commit()

        book = Books(
            title=book_title,
            author=request.form["author"],
            description=request.form["description"],
        )
        db.session.add(book)
        db.session.commit()
        return render_template("success.html", name=book_title, token=token_value)
    return render_template("add.html")

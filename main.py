from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)

# :ost to store book objects
# all_books = []

# Database
class Base(DeclarativeBase):
    pass

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

# Extension
db = SQLAlchemy(model_class=Base)

# Initialize the app with the extension
db.init_app(app)

# Define Model
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    review: Mapped[float] = mapped_column(Float, nullable=False)
# Create the table schema in the database, Requires application context
# with app.app_context():
#     db.create_all()

@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        all_books = [book for book in result.scalars()]
        print(all_books)
    return render_template("index.html", books=all_books)


@app.route("/add", methods={"GET", "POST"})
def add():
    if request.method == "POST":
        with app.app_context():
            new_book = Book(title=request.form.get("title"), author=request.form.get("author"), review=request.form.get("rating"))
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for("home"))
        # book = {
        #     "title" : request.form.get("title"),
        #     "author": request.form.get("author"),
        #     "rating": float(request.form.get("rating"))
        # }
        # all_books.append(book)
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)


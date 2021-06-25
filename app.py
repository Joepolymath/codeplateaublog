from enum import unique
from logging import debug
from flask import Flask, render_template, request
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
import os

from werkzeug.utils import redirect


app = Flask(__name__)
# finding the current app path. (Location of this file)
project_dir = os.path.dirname(os.path.abspath(__file__))

# creating a database file (bookdatabase.db) in the above found path.
database_file = "sqlite:///{}".format(os.path.join(project_dir, "blogposts.db"))

# connecting the database file (bookdatabase.db) to the sqlalchemy dependency.
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# connecting this app.py file to the sqlalchemy
db = SQLAlchemy(app)

class Posts(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    content = db.Column(db.String(700), unique=False, nullable=False)

    def __repr__(self):
        return f"Title: {self.title}"

@app.route('/')
def home():
    posts = Posts.query.all()

    return render_template("index.html", posts = posts)

@app.route('/newpost', methods=["GET", "POST"])
def newpost():
    if request.form:
        title = request.form.get('title')
        content = request.form.get('content')
        post = Posts(title=title, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("newpost.html")

@app.route('/confirm/<title>')
def confirm(title):
    selected_post = Posts.query.filter_by(title=title).first()
    return render_template("confirm.html", selected_post=selected_post)


@app.route('/delete/<title>', methods=["GET", "POST"])
def delete(title):
    post = Posts.query.filter_by(title=title).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit/<title>', methods=["POST", "GET"])
def edit(title):
    selected_post = Posts.query.filter_by(title=title).first()
    if request.form:
        selected_post.title = request.form.get('title')
        selected_post.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", selected_post=selected_post)

if __name__ == "__main__":
    app.run(debug=True)
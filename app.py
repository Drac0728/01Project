from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20), nullable = False)
    content = db.Column(db.String(), nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

@app.route('/')
def home():
    posts = Post.query.order_by(Post.date.desc())
    return render_template("index.html", posts = posts)

@app.route('/Addpost', methods = ['GET','POST'])
def addpost():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        post = Post(title = title, content = content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("post.html")

if __name__ == "__main__":
    app.run(debug = True)


from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import datetime


app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="neobaud",
    password="600*$53IfrH!",
    hostname="neobaud.mysql.pythonanywhere-services.com",
    databasename="neobaud$recommender",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "aslkdjfasldkjfasldkjlsdk"
login_manager = LoginManager()
login_manager.init_app(app)

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(128))
    rating = db.Column(db.Integer)
    posted = db.Column(db.DateTime, default=datetime.now)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    item = db.relationship('Item', foreign_keys=item_id)

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return self.username


class Item(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4096))
    category = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments = Comment.query.all())
        #return render_template("main_page.html", comments = Comment.query.all(), timestamp=datetime.now())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    comment = Comment(content=request.form["contents"], commenter=current_user)

    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('index'))

@app.route("/item_entry/", methods=["GET", "POST"])
def test():
    if request.method == 'POST':


        # Check if it is in the database already
        if request.form["name"] == '' or request.form["category"] == '':
            flash('Enter a name and category')
        elif db.session.query(Item.name).filter_by(name=request.form["name"]).first() == None:
            item = Item(name=request.form["name"], category=request.form["category"])
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('item_entry'))
        else:
            flash("Item Already Exists")
    return render_template("item_entry.html", items=Item.query.all(), error=True)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
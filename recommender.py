

from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="neobaud",
    password="600*$53IfrH!",
    hostname="neobaud.mysql.pythonanywhere-services.com",
    #hostname="127.0.0.1:3306",
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
    image = db.Column(db.String(4096), default='static/thumbs/not_found.png')

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

'''
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        #ratings = Comment.query.
        ratings_ave = db.session.query(Item.name, func.avg(Comment.rating).label('average')).outerjoin(Comment, Comment.item_id == Item.id).group_by(Comment.item_id)

        return render_template("main_page.html", comments = ratings_ave)

    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    comment = Comment(content=request.form["contents"], commenter=current_user)

    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))
'''

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

#@app.route("/item_entry/", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        # Check if it is in the database already

        if request.form["name"] == '' or request.form["category"] == '':
            flash('Enter a name and category')
        elif db.session.query(Item.name).filter_by(name=request.form["name"]).first() == None:
            item = Item(name=request.form["name"], category=request.form["category"])
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            flash("Item Already Exists")
            return redirect(url_for('index'))

        return redirect(url_for('index'))
    

    if request.form.get('search'):
        flash('search it %s' % request.form.get('search'))
        
        
    ratings_ave = db.session.query(Item.name, Item.id, Item.image, func.avg(Comment.rating).label('average')).outerjoin(Comment, Comment.item_id == Item.id).group_by(Comment.item_id)
    averages = {r.id : (str(round(r.average,1)) if r.average != None else "0") for r in ratings_ave  }
        
    if current_user.is_authenticated:
        ratings = Comment.query.filter_by(commenter_id = current_user.id).all()
        if ratings != None:
            ratings = {r.item_id : r.rating for r in ratings}
    else:
        ratings = {}

    f = request.args.get('search').lower() if request.args.get('search') != None else ''
    filter_items = []
    categories = set([])
    for item in Item.query.all():
        categories.add(item.category)
        if f in item.name.lower() and (request.args.get('category', 'All') == 'All' or request.args.get('category') == item.category):
            filter_items.append(item)
    #filter_items = []
        
    return render_template("item_entry.html", items=filter_items, ratings = ratings, averages = averages, categories=categories, args=request.args)

@app.route('/rate/', methods=('GET', 'POST'))
@login_required
def rate():
    rating = int(request.form["rating"])
    item = int(request.form["item"])
    # If user and rating already exist then update
    rate_db = db.session.query(Comment).filter_by(commenter_id=current_user.id, item_id = item).first()
    if rate_db != None:
        rate_db.rating = rating
    else:
        db.session.add(Comment(commenter_id = current_user.id, item_id = item, rating = rating))
    db.session.commit()
    return 'Rate item: %d,  User: %d, rating: %d' % (item, current_user.id, rating)

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.session.query(User).filter_by(username=request.form["username"]).first() is not None:
            error = 'User {} is already registered.'.format(username)
        if error is None:
            db.session.add(User(username=username, password_hash=generate_password_hash(password)))
            db.session.commit()
            return redirect(url_for('login'))

        flash(error)

    return render_template('register.html')


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

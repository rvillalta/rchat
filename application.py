from flask import Flask, render_template, redirect, url_for
from wtform_fields import *
from models import *
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

#Configure App
app = Flask(__name__)
app.secret_key = 'replace later'

#Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gtosymwiyznegn:db668c070de6d21fc461221ad6b3b0e1b0e5aa86763061bb0dc2f450f7d145bf@ec2-34-233-43-35.compute-1.amazonaws.com:5432/d4etelcs346mk5'
db = SQLAlchemy(app)

#Configure Flash-Login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/", methods=["GET", "POST"])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username    = reg_form.username.data
        password    = reg_form.password.data

        #Hash password
        hashed_pswd = pbkdf2_sha256.hash(password)

        #Add user to DB
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("index.html", form=reg_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    #Allow login if validation succsess
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))
    return render_template('login.html', form=login_form)

@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat() :
    if not current_user.is_authenticated:
        pass
    return "Chat with me!"

@app.route('/logout')
def logout():
    logout_user()
    return "Logged out using flask-login"


if __name__ == "__main__":
    app.run(debug=True)

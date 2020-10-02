from flask import Flask, render_template, redirect, url_for
from wtform_fields import *
from models import *


#Configure App
app = Flask(__name__)
app.secret_key = 'replace later'

#Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gtosymwiyznegn:db668c070de6d21fc461221ad6b3b0e1b0e5aa86763061bb0dc2f450f7d145bf@ec2-34-233-43-35.compute-1.amazonaws.com:5432/d4etelcs346mk5'
db = SQLAlchemy(app)

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
        return "Loggin in, finally"
    return render_template('login.html', form=login_form)

if __name__ == "__main__":
    app.run(debug=True)

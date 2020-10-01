from flask import Flask, render_template
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

        #Add user to DB
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted into DB !"
    return render_template("index.html", form=reg_form)

if __name__ == "__main__":
    app.run(debug=True)

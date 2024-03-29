from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create Flask instance
app = Flask(__name__)
# Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Secret key
app.config['SECRET_KEY'] = 'you want to change it in the future'

db = SQLAlchemy(app)


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create A String
    def __repr__(self):
        return f'<Name {self.name}'


# Create Form Class
# Create Form Class
class NameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')


# Create a routes
# Databases routes
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash('User added to database successfully!')
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form, name=name, our_users=our_users)


# Static page
@app.route('/')
def index():
    first_name = 'Kuba'
    stuff = "This is <strong> Bold</strong> Text"
    favorite_pizza = ['Pepperoni', 'Margherita', 41]
    return render_template('index.html',
                           first_name=first_name,
                           stuff=stuff,
                           favorite_pizza=favorite_pizza)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


# Create Name Page with Form
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form Submitted Successfully!')
    return render_template('name.html', name=name, form=form)


# Custom Error Pages
# Invalid URL 404 error
@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


# Invalid URL 500 error
@app.errorhandler(500)
def page_not_found():
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)

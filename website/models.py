# this file is going to store
# two database models that we are going to have

# from current package import db
from . import db
# importing custom class that we can inherit
# that will give our user object specific
from flask_login import UserMixin
# func.now gets the current date and stores this date
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(255))
    # defining the date when this note was created
    # we don't need to specify date field, just sqlalchemy
    # takes care of this and whenever we create a new
    # note it will automatically add the date for us
    # func.now gets the current date and stores this date
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # all notes must belong to user and different information
    # must associate with different users (one-to-many relationship)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


# set up User model that going to store
# all user's information in a schema below
class User(db.Model, UserMixin):
    # defining all columns (schema) we want
    # to have stored in this "User" table
    id = db.Column(db.Integer, primary_key=True)
    # db.Integer or db. String is defining type of column
    # primary key is way to uniquely identify this object
    email = db.Column(db.String(150), unique=True)
    # unique=True means that users cant have same email
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # this field will store all notes
    # we create referencing to another db model "Note"
    notes = db.relationship("Note")

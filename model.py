"""Models and database functions for Scheduling App."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Part 1: Compose ORM

class Unit(db.Model):

    __tablename__ = "units"

    unit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    unit_name = db.Column(db.String(64), nullable=False)
    
   

    team = db.relationship("Team", backref=db.backref("units", order_by=unit_id))


class Team(db.Model):

    __tablename__ = "teams"

    team_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    team_name = db.Column(db.String(64), nullable=False)
    team_size = db.Column(db.String(64), nullable=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), 
                        nullable=False)

    
    course = db.relationship("Course", backref=db.backref("teams", 
                                order_by=team_id))



class Course(db.Model):

    __tablename__ = "courses"

    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_name = db.Column(db.String(64), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), 
                         nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), 
                        nullable=False)
    training_period = db.Column(db.String(64), 
                                db.ForeignKey('training_period.type'), 
                                nullable=False)


  


    training_period = db.relationship("TrainingPeriod", backref=db.backref
                  ("courses", order_by=course_id))
class TrainingPeriod(db.Model):

    __tablename__ = "training_period"

    training_type = db.Column(db.String(64), nullable=False, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    

    




class Staff(db.Model):

    __tablename__ = "staff"

    staff_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    staff_role = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    username = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(30), nullable=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):

        return '<Staff %r>' % self.username



class Building(db.Model):

    __tablename__ = "buildings"

    bldg_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    bldg_name = db.Column(db.String(64), nullable=False)

 



class Room(db.Model):

    __tablename__ = "rooms"

    room_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    room_num = db.Column(db.String(30), nullable=False)
    capacity = db.Column(db.Integer, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'),
                          nullable=False)
    bldg_id = db.Column(db.Integer, db.ForeignKey('buildings.bldg_id'), 
                        nullable=False)

    



# user = db.relationship("User", backref=db.backref("ratings", order_by=rating_id))

# movie = db.relationship("Movie", backref=db.backref("ratings", order_by=rating_id))
# End Part 1
##############################################################################
# Helper functions


def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedule.db'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
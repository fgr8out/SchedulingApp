from flask import Flask, flash, json, redirect, render_template, request, send_file, session
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime, timedelta
from jinja2 import StrictUndefined
from model import connect_to_db, db
from model import *
from twilio.rest import TwilioRestClient
import os
from secrets import TW_ACCOUNT_SID, TW_AUTH_TOKEN, TWILIO_NUMBER
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "\xf0\x89\r\xbd/m\x9f<\xfd\xab8\xf00\xf8\x07t\x02\xec9\xd1\xa5&`B"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


print TW_ACCOUNT_SID, TW_AUTH_TOKEN, TWILIO_NUMBER

@app.route('/')
def splash_login():
    """Login Page"""


    return render_template("login.html")

@app.route('/process_login', methods=['POST'])
def login_user():
    """Log in user based on db info"""

    email = request.form["email"]
    password = request.form["password"]

    print email
    print password

    user = Staff.query.filter_by(email=email).first()
    if user.password == password:
        session["staff_id"] = user.staff_id 
        session["username"] = user.fname  
        print session["staff_id"]

    return redirect('/schedule')

@app.route('/logout', methods=['POST'])
def logout_user():
    """Logout of session"""


    session["staff_id"] = []
    session["username"] = None 

    print session["staff_id"]
    print session["username"]
    return redirect('/')



@app.route('/schedule')
def choose_schedule():
    """Main Scheduling Page"""

    teams = Team.query.all()
    units = Unit.query.all()
    staff = Staff.query.all()
    trainings = Training.query.all()

    return render_template("schedule.html", teams=teams, trainings=trainings,
                           units=units, staff=staff)


@app.route('/submit_schedule', methods=['POST'])
def submit_schedule():
    "Submit/Post webform to db"

    team = request.form['team_name']
    training = request.form['training_name']
    staff_id = request.form['staff_id']
    start_date = request.form['start_date']
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    start_time = request.form['start_time']
    start_time = datetime.strptime(start_time, '%H:%M')
    end_time = request.form['end_time']
    end_time = datetime.strptime(end_time, '%H:%M')

    # Creates new user in DB
    new_training = TrainingAssignment(
        team_id=team,
        training_id=training,
        staff_id=staff_id,
        start_date=start_date,
        start_time=start_time,
        end_time=end_time)

    db.session.add(new_training)
    db.session.commit()

    staff_poc = Staff.query.filter_by(staff_id=staff_id).first()    

    poc_phone = staff_poc.work_phone

    client = TwilioRestClient(TW_ACCOUNT_SID, TW_AUTH_TOKEN)
    message = client.messages.create(to="+1{}".format(poc_phone), 
                                        from_=TWILIO_NUMBER,
                                        body= "You have been schedule for {} training on {} starting {}.".format (training, start_date, start_time))

    
    flash("Schedule Request has been created for {}".format(team))
    return redirect("/submit_schedule.html")


@app.route('/dashboard')
def process_request():
    """Show result of schedule choices on dashboard."""

    if session["staff_id"] == "ADMIN":
        assignments = TrainingAssignment.query.all()

    else: 
        assignments = TrainingAssignment.query.filter_by(staff_id = session["staff_id"]).all()

    print assignments
    print session["staff_id"]


    return render_template("dashboard.html", assignments=assignments)
# #############################################################
# # Jinja Filter

# @app.template_filter('datetime')
# def _format_datetime(dt, format=None, trip_end=False):
#     """Formats a datetime object for display """

#     if trip_end:
#         dt = dt - timedelta(1)

#     if format == 'time':
#         dt = datetime.strftime(dt, '%-I:%M %p')
#     elif format == 'date':
#         dt = datetime.strftime(dt, '%b %-d, %Y')
#     elif format == 'date-short':
#         dt = datetime.strftime(dt, '%b %-d')
#     elif format == 'datetime pretty':
#         dt = datetime.strftime(dt, '%-I:%M %p, %b %d, %Y')
#     else:
#         dt = datetime.strftime(dt, '%Y-%m-%dT%H:%M:%SZ')

# return dt
###############################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()

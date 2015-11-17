from flask import Flask, flash, json, redirect, render_template, request, send_file, session
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime, timedelta
from jinja2 import StrictUndefined
from model import connect_to_db, db
from model import *

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def splash_login():
    """Login Page"""


    return render_template("login.html")


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
    print team
    training = request.form['training_name']
    print training
    start_date = request.form['start_date']
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    print type(start_date)
    end_date = request.form['end_date']
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    print type(end_date)
    start_time = request.form['start_time']
    start_time = datetime.strptime(start_time, '%H:%M')
    print type(start_time)
    end_time = request.form['end_time']
    end_time = datetime.strptime(end_time, '%H:%M')
    print type(end_time)

        

        
        
    #Creates new user in DB
    new_training = TrainingAssignment(
                                 team_id=team,
                                 training_id=training,
                                 start_date=start_date,
                                 end_date=end_date,
                                 start_time=start_time,
                                 end_time=end_time)

    db.session.add(new_training)
    db.session.commit()


    flash("Schedule Request has been created for {}".format(team))

    return redirect("/schedule.html")



@app.route('/dashboard')
def process_request():
    """Show result of schedule choices on dashboard."""


    return render_template("dashboard.html")



# @app.route("/login", methods=['GET'])
# def login_page():
#     """Displays login page"""

#     return render_template("login.html")



# @app.route("/login", methods=['POST'])
# def login():
#     """Logs in the user, or denies access"""

#     email = request.form.get("email")
#     password = request.form.get("password")
    
#     user = User.authenticate(email, password)

#     if user:
#         session["user_id"] = user.user_id
#         session["fname"] = user.fname
#         return redirect("/trips")

#     else:
#         flash("Your information could not be found in the system. Try again or sign up!")
#         return redirect("/login")


# @app.route('/register', methods=['POST'])
# def register_process():
#     """Process registration."""

#     # Get form variables
#     email = request.form["email"]
#     password = request.form["password"]
   

#     new_user = User(email=email, password=password)

#     db.session.add(new_user)
#     db.session.commit()

#     flash("User %s added." % email)
#     return redirect("/")


# @app.route('/login', methods=['GET'])
# def login_form():
#     """Show login form."""

#     return render_template("login_form.html")


# @app.route('/login', methods=['POST'])
# def login_process():
#     """Process login."""

#     # Get form variables
#     email = request.form["email"]
#     password = request.form["password"]

#     user = User.query.filter_by(email=email).first()

#     if not user:
#         flash("No such user")
#         return redirect("/login")

#     if user.password != password:
#         flash("Incorrect password")
#         return redirect("/login")

#     session["user_id"] = user.user_id

#     flash("Logged in")
#     return redirect("/users/%s" % user.user_id)


# @app.route('/logout')
# def logout():
#     """Log out."""

#     del session["user_id"]
#     flash("Logged Out.")
#     return redirect("/")


# @app.route("/users")
# def user_list():
#     """Show list of users."""

#     users = User.query.all()
#     return render_template("user_list.html", users=users)


# @app.route("/users/<int:user_id>")
# def user_detail(user_id):
#     """Show info about user."""

#     user = User.query.get(user_id)
#     return render_template("user.html", user=user)


# @app.route("/movies")
# def movie_list():
#     """Show list of movies."""

#     movies = Movie.query.order_by('title').all()
#     return render_template("movie_list.html", movies=movies)


# @app.route("/movies/<int:movie_id>", methods=['GET'])
# def movie_detail(movie_id):
#     """Show info about movie.

#     If a user is logged in, let them add/edit a rating.
#     """

#     movie = Movie.query.get(movie_id)

#     user_id = session.get("user_id")

#     if user_id:
#         user_rating = Rating.query.filter_by(
#             movie_id=movie_id, user_id=user_id).first()

#     else:
#         user_rating = None

#     return render_template("movie.html",
#                            movie=movie,
#                            user_rating=user_rating)


# @app.route("/movies/<int:movie_id>", methods=['POST'])
# def movie_detail_process(movie_id):
#     """Add/edit a rating."""

#     # Get form variables
#     score = int(request.form["score"])

#     user_id = session.get("user_id")
#     if not user_id:
#         raise Exception("No user logged in.")

#     rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

#     if rating:
#         rating.score = score
#         flash("Rating updated.")

#     else:
#         rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
#         flash("Rating added.")
#         db.session.add(rating)

#     db.session.commit()

#     return redirect("/movies/%s" % movie_id)

# @app.route("/pdf", methods=["POST"])
# def generate_pdf():
#     """Generates a PDF of the itinerary"""

#     trip_id = int(request.form['tripId'])
#     trip = Trip.query.get(trip_id)
#     filename = "itinerary%d.pdf" % (trip_id)
#     trip.generate_itinerary(filename)

#     response_dict = {'filename': filename}
#     response = json.dumps(response_dict)

#     return response

# @app.route("/send_text", methods=["POST", "GET"])
# def send_reminders():
#     """Sends reminders to trip viewers"""

#     trip_id = int(request.form['tripId'])
#     trip = Trip.query.get(trip_id)

#     trip.send_SMS(tw_sid, tw_token)

#     return "Success"


# @app.route("/itinerary<int:trip_id>", methods=['GET', 'POST'])
# def show_pdf(trip_id):
#     """Displays the PDF itinerary"""

#     filename = 'itinerary%r.pdf' % (trip_id)
#     itinerary = open(filename, 'rb')

#     return send_file(itinerary)

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
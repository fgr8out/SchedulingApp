"""NCCC Training Schedule"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session 

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db

from model import Building, Course, TrainingPeriodCourseAvailabilty, Room, Staff, Team, TrainingPeriod, Unit



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """This is a page to test if there is a homepage"""


    # testperiod = Course.query.filter(Course.course_id == 1).first()
    # cycle = Course.query.filter(Course.course_id<=20).all()
    # print cycle

    # testteam = Team.query.filter(Team.team_id=='O1').first()
    # teams = Team.query.filter(Team.team_name.like('%Oak%')).all()
  
    # print cycle
    # for course in cycle
    #     course.
    # for team in teams:
        # team.unit_id = "oak"
  
    # db.session.commit()


    # return render_template("homepage.html")






# @app.route('/schedule')
# def schedule():
#     """Page to choose scheduling options."""


#     return render_template("schedule.html")

   
# @app.route('/dashboard')
# def somethingcool():
#    """Show results from schedule picking on this lovely dashboard"""

#     # users = User.query.all()

#     return render_template("dashboard.html")


# @app.route('/login')
# def show_login():
#     """Show login page"""
#     return render_template("login.html")



# @app.route('/handle-login', methods=['POST'])
# def handle_login():
#     """Process login form"""

#     username = request.form['username']
#     password = request.form['password']

#     user = User.query.filter_by(email = username).first()
#     if user:
#         if user.password == password:
#             session['user'] = username
#             flash("Logged in as %s" % username)
#             return redirect('user_info/%s' % user.user_id)
#         else: 
#             flash("Wrong password!")
#             return redirect('/')

#     else:
#         flash("Sorry, this username does not exist!")
#         return redirect('/')


# @app.route('/user_info/<int:user_id>')
# def user_info(user_id):
#     user = User.query.get(user_id)
#     return render_template("user_info.html", user=user)





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
"""Utility file to seed schedule database various seed files/"""


from model import Building
from model import Course
from model import TrainingPeriodCourseAvailabilty
from model import Room
from model import Staff
from model import Team
from model import TrainingPeriod
from model import Unit



from model import connect_to_db, db
from server import app
from datetime import datetime


def load_buildings():
    """Load users from building into database."""

    print "Buildings"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Building.query.delete()

    # Read building file and insert data
    for row in open("seed_data/building"):
        row = row.rstrip()
        bldg_id , bldg_name = row.split(",")

        building = Building(bldg_id=bldg_id,
                    bldg_name=bldg_name)

        # We need to add to the session or it won't ever be stored
        db.session.add(building)

    # Once we're done, we should commit our work
    db.session.commit()


def load_courses():
    """Load courses from course.csv into database."""

    print "Courses"

    Course.query.delete()


    for row in open("seed_data/course"):
        row = row.strip()
        items = row.split(",")

        course = Course(course_name = items[0])

        db.session.add(course)

    db.session.commit()


def load_CourseAvailability():
    """Assoc table to connect course availability by training period into database."""

    print "Course Availability"
    
    TrainingPeriodCourseAvailabilty.query.delete()

    for row in open("seed_data/course.availability"):
        row = row.strip()
        items = row.split(",")

        availability = TrainingPeriodCourseAvailability(trackcourse=items[0])

        db.session.add(course.availabilty)

    db.session.commit()


def load_room():
    """Load room numbers from room.csv into database."""

    print "rooms"
    
    Room.query.delete()

    for row in open("seed_data/room"):
        row = row.strip()
        items = row.split(",")

        room = Room(room_loc=items[0],
                        capacity=items[1])

        db.session.add(room)

    db.session.commit()

def load_staff():
    """Load staff information from staff.csv into database."""

    print "staff"
    
    Staff.query.delete()

    for row in open("seed_data/staff"):
        row = row.strip()
        items = row.split(",")

        staff = Staff(staff_id=items[0],
                        role=items[1],
                        firstname=items[2],
                        lastname=items[3])

        db.session.add(staff)

    db.session.commit()


def load_team():
    """Load teams info from team.csv into database."""

    print "teams"
    
    Team.query.delete()

    for row in open("seed_data/team"):
        row = row.strip()
        items = row.split(",")

        team = Team(team_id=items[0],
                    team_name=items[1],
                    team_size=items[2])

        db.session.add(team)

    db.session.commit()


def load_trainingperiod():
    """Load training periods from trainingperiod.csv into database."""

    print "training period"
    
    TrainingPeriod.query.delete()

    for row in open("seed_data/trainingperiod"):
        row = row.strip()
        items = row.split(",")
        start_date = items[1]
        end_date = items[2]

        start_date = datetime.strptime(start_date, '%b/%d/%Y')
        end_date = datetime.strptime(end_date, '%b/%d/%Y')

        trainingperiod = TrainingPeriod(type_id=items[0],
                        start_date=start_date,
                        end_date=end_date,
                        cycle=items[3])

           

        db.session.add(trainingperiod)

    db.session.commit()


def load_unit():
    """Load units from unit.csv into database."""

    print "units"
    
    Unit.query.delete()

    for row in open("seed_data/unit"):
        row = row.strip()
        items = row.split(",")

        unit = Unit(unit_id=items[0],
                    unit_name=items[1])
                    

        db.session.add(unit)

        db.session.commit()
    

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_buildings()
    # load_courses()
    # load_CourseAvailability()
    # load_room()
    # load_staff()
    # load_team()
    load_trainingperiod()
    # load_unit()
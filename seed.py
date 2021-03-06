"""Utility file to seed schedule database various seed files/"""

from model import Building
from model import Training
from model import Room
from model import Staff
from model import Team
from model import Unit
from model import TrainingAssignment
# from model import TrainingPeriod
# from model import TrainingAvailability
# from model import TrainingByDatetime
from model import connect_to_db, db
from server import app
from datetime import datetime, time


def load_Building():
    """Load building names into database."""

    print "Buildings"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Building.query.delete()

    # Read building file and insert data
    for row in open("seed_data/building"):
        row = row.rstrip()
        bldg_id, bldg_name = row.split(",")

        building = Building(bldg_id=bldg_id,
                            bldg_name=bldg_name)

        # We need to add to the session or it won't ever be stored
        db.session.add(building)

    # Once we're done, we should commit our work
    db.session.commit()


def load_Training():
    """Load training options from training.csv into database."""

    print "Trainings"

    Training.query.delete()

    for row in open("seed_data/training.csv"):
        row = row.strip()
        items = row.split(",")

        training = Training(training_id=items[0],
                            training_name=items[1],
                            description=items[2],
                            duration=items[3])

        db.session.add(training)

        db.session.commit()


# def load_TrainingAssignment():
#     """Association table to connect training assignment by team_id"""

#     print "Training Assignment"

#     TrainingAssignment.query.delete()

#     for row in open("seed_data/training.assignment.csv"):
#         row = row.strip()
#         items = row.split(",")
#         print len(items)
#         assignment_id = items[0]
#         # team_id 
#         training_id = items[1]

#         start_date = items[2]
#         end_date = items[3]
#         start_time = items[4]
#         end_time =  items[5]

#         start_date = datetime.strptime(start_date, '%m/%d/%y')
#         end_date = datetime.strptime(end_date, '%m/%d/%y')

#         start_time = datetime.strptime(start_time, '%H:%M')
#         end_time = datetime.strptime(end_time, '%H:%M')

#         trainingassignment = TrainingAssignment(assignment_id=assignment_id,
#                             # team_id=team_id,
#                             training_id=training_id,
#                             # staff_id=staff_id,
#                             start_date=start_date,
#                             end_date=end_date,
#                             start_time=items,
#                             end_time=items)


#         db.session.add(trainingassignment)

#     db.session.commit()



def load_Room():
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


def load_Staff():
    """Load staff information from staff.csv into database."""

    print "staff"

    Staff.query.delete()

    for row in open("seed_data/staff"):
        row = row.strip()
        items = row.split(",")

        staff = Staff(staff_id=items[0],
                      staff_role=items[1],
                      fname=items[2],
                      lname=items[3],
                      email=items[4],
                      username=items[5],
                      password=items[6],
                      work_phone=items[7])

        db.session.add(staff)

    db.session.commit()


def load_Team():
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


def load_Unit():
    """Load units from units into database."""

    print "units"

    Unit.query.delete()

    for row in open("seed_data/units"):
        row = row.strip()
        items = row.split(",")

        unit = Unit(unit_name=items[0])

        db.session.add(unit)

        db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_Building()
    load_Training()
    load_Room()
    load_Staff()
    load_Team()
    load_Unit()

# load_TrainingPeriod()
# load_TrainingAvailability()
 # load_TrainingAssignment()
################################################################################
# Functions to be used at a later date

# def load_TrainingAvailability():
#     """Assocation table to connect course availability by training period"""

#     print "Training Availability"

#     CourseAvailability.query.delete()

#     for row in open("seed_data/course.availability"):
#         row = row.strip()
#         items = row.split(",")

#         availability = CourseAvailability(trackcourse=items[0])

#         db.session.add(availabilty)

#     db.session.commit()


# def load_TrainingPeriod():
#     """Load training periods from trainingperiod.csv into database."""

#     print "training period"

#     TrainingPeriod.query.delete()

#     for row in open("seed_data/trainingperiod"):
#         row = row.strip()
#         items = row.split(",")
#         start_date = items[1]
#         end_date = items[2]

#         start_date = datetime.strptime(start_date, '%b/%d/%Y')
#         end_date = datetime.strptime(end_date, '%b/%d/%Y')

#         trainingperiod = TrainingPeriod(type_id=items[0],
#                         start_date=start_date,
#                         end_date=end_date,
#                         cycle=items[3])


#         db.session.add(trainingperiod)

#     db.session.commit()

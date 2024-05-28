# Copyright © 2023, Indiana University
# BSD 3-Clause License

from flask import Flask, render_template, redirect, url_for, request
from flaskapp import database
import html

app = Flask(__name__)

def get_all_events():
    """The purpose of this function has the task of opening the events table and grabbing the content of the table."""
    events_from_db = database.get_events()
    return events_from_db

def get_all_venues():
    """The purpose of this function has the task of opening the venues table and grabbing the content of the table."""
    venues_from_db = database.get_venues()
    return venues_from_db

def get_all_people():
    """The purpose of this function has the task of opening the people table and grabbing the content of the table."""
    people_from_db = database.get_people()
    return people_from_db

def set_all_people(name,address,email,date_of_birth,phone,role):
    """The purpose of this function is to refer to the correct function on database.py and when a person would 
    like to add to the table it writes that data back out to that function to the table."""
    #Rather than having one function for adding people to the table the add_person route will referenced this function
    # in case this function needs to be referneced by another route in the future and in order to stay organized#
    database.add_person(name,address,email,date_of_birth,phone,role)

def set_all_venues(name,address,phone,fee,attendees_capacity):
    """The purpose of this function is to refer to the correct function on database.py and when a person would 
    like to add to the table it writes that data back out to that function to the table."""
    #Rather than having one function for adding venues to the table the add_person route will referenced this function
    #in case this function needs to be referneced by another route in the future and in order to stay organized#
    database.add_venue(name,address,phone,fee,attendees_capacity)
    

def set_all_events(name,date,venue_id,start_time,end_time,invitation,image_path,attendees,planner_id,host_id,rental_items,notes):
    """The purpose of this function is to refer to the correct function on database.py and when a person would 
    like to add to the table it writes that data back out to that function to the table."""
    #Rather than having one function for adding events to the table the add_person route will referenced this function
    # in case this function needs to be referneced by another route in the future and in order to stay organized#
    database.add_event(name,date,venue_id,start_time,end_time,invitation,image_path,attendees,planner_id,host_id,rental_items,notes)

def check_people(name,address,email,date_of_birth,phone,role):
    """Function to validate people form"""
    error = ""
    msg = []
    if not name:
        msg.append("Name is missing!")
    if len(name) > 30:
        msg.append("Name is too long!")
    if not address:
        msg.append("Address is missing!")
    if not email:
        msg.append("Email is missing!")
    if not date_of_birth:
        msg.append("Date of birth is missing!")
    if not phone:
        msg.append("Phone number is missing!")
    if not role:
        msg.append("Role is missing!")
    return error

def check_venues(name,address,phone,fee,attendees_capacity):
    """Function to validate venue form"""
    error = ""
    msg = []
    if not name:
        msg.append("Name is missing!")
    if len(name) > 30:
        msg.append("Name is too long!")
    if not address:
        msg.append("Address is missing!")
    if not phone:
        msg.append("Phone number is missing!")
    if not fee:
        msg.append("Fee is missing!")
    if not attendees_capacity:
        msg.append("Maximum capacity for venue is missing!")
    return error

def check_events(name,date,venue_id,start_time,end_time,invitation,image_path,attendees,planner_id,host_id,rental_items,notes):
    """Function to validate event form"""
    error = ""
    msg = []
    if not name:
        msg.append("Name is missing!")
    if len(name) > 40:
        msg.append("Name is too long!")
    if not date:
        msg.append("Date is missing!")
    if not venue_id:
        msg.append("Venue ID is missing!")
    if not start_time:
        msg.append("Start time is missing!")
    if not end_time:
        msg.append("End time is missing!")
    if not invitation:
        msg.append("Invitation is missing!")
    if not image_path:
        msg.append("Image Path is missing!")
    if not attendees:
        msg.append("Attendees is missing!")
    if not planner_id:
        msg.append("Planner ID is missing!")
    if not host_id:
        msg.append("Host ID is missing!")
    if not rental_items:
        msg.append("Rental Items are missing!")
    if not notes:
        msg.append("Notes are missing!")
    return error

@app.route("/")
def index():
    """function to render the index.html template"""
    return render_template("index.html")

@app.route("/events/")
@app.route("/events/<event_id>")
def show_events(event_id=None):
    """After referencing the function that references get_all_events, this
    function has the purpose of rendering the correct template for events.html and event.html"""
    #event_id is now numerical auto increment rather than being "name"
    #each variable is named in order to reference it in the event.html, so different tables can be used when creating the final form
    if (event_id):
        event=database.get_event((event_id))
        venues=database.get_venue_name_db((event_id))
        hosts=database.get_host((event_id))
        planners=database.get_planner((event_id))
        attendees=database.get_attendees((event_id))
        customers=database.get_customers((event_id))
        return render_template('event.html', event=event,event_id=event_id,venues=venues,hosts=hosts,planners=planners,attendees=attendees,customers=customers)
    all_events = get_all_events()
    return render_template('events.html', events = all_events)
    
@app.route("/venues/")
def show_venues():
    """This function renders veneus.html and shows all the evenues."""
    venues = get_all_venues()
    return render_template('venues.html', venues=venues)

@app.route("/people/")
def show_people():
    """This function renders people.html and shows all people."""
    people = get_all_people()
    return render_template('people.html', people=people)

@app.route("/people/add", methods=["GET", "POST"])
def add_person(person_id=None):
    """This function has the purpose of when a person adds a new person via the form it 
    rquests the form and properly writes it back out to another function which writes to the database."""
    if request.method == "POST":
        name = html.escape(request.form['name']),
        address = html.escape(request.form['address']),
        email = html.escape(request.form['email']),
        date_of_birth = request.form['date_of_birth'],
        phone = html.escape(request.form['phone']),
        role =  request.form['role']
        error=check_people(name,address,email,date_of_birth,phone,role)
        if error:
            people=database.get_people(person_id)
            return render_template('people_form.html', name=name, address=address,
                                   email=email, date_of_birth=date_of_birth,
                                   phone=phone, role=role, person_id=person_id,
                                   error=error)
        set_all_people(name,address,email,date_of_birth,phone,role)
        return redirect(url_for("show_people", person_id=person_id))
    else:
        people=database.get_person(person_id)
        return render_template("people_form.html", people=people)

@app.route("/venues/add", methods=["GET", "POST"])
def add_venues(venue_id=None):
    """This function has the purpose of when a person adds a new venue via the form it 
    rquests the form and properly writes it back out to another function whoch writes to the database."""
    if request.method == "POST":
        name = html.escape(request.form['name']),
        address = html.escape(request.form['address']),
        phone = request.form['phone'],
        fee = request.form['fee'],
        attendees_capacity = request.form['attendees_capacity']
        error=check_venues(name,address,phone,fee,attendees_capacity)
        #need an if statment for handling errors which is referencing a function created above, if error is found a msg is appended and displayed.
        if error:
            venues=database.get_venues(venue_id)
            return render_template('venue_form.html', name=name, address=address,
                                   phone=phone, fee=fee, attendees_capacity=attendees_capacity,
                                   venue_id=venue_id, error=error)
        set_all_venues(name,address,phone,fee,attendees_capacity)
        return redirect(url_for("show_venues", venue_id=venue_id))
    else:
        venues=database.get_venue(venue_id)
        return render_template("venue_form.html", venues=venues)
    
@app.route("/events/add", methods=["GET", "POST"])
def add_events(event_id=None):
    """This function has the purpose of when a person adds a new event via the form it 
    rquests the form and properly writes it back out to another function which adds to table in database."""
    if request.method == "POST":
        name = html.escape(request.form['name']),
        date = request.form['date'],
        venue_id = request.form['venue_id'],
        start_time = request.form['start_time'],
        end_time = request.form['end_time'],
        invitation = html.escape(request.form['invitation']),
        image_path = html.escape(request.form['image_path']),
        attendees = request.form['attendees'],
        planner_id =  request.form['planner_id'],
        host_id =  request.form['host_id'],
        rental_items =  html.escape(request.form['rental_items']),
        notes = html.escape(request.form['notes'])
        error=check_events(name,date,venue_id,start_time,end_time,invitation,image_path,attendees,planner_id,host_id,rental_items,notes)
        if error:
            events=database.get_events(event_id)
            return render_template('event_form.html', name=name, date=date, venue_id=venue_id, 
                                   start_time=start_time, end_time=end_time, invitation=invitation,
                                   image_path=image_path, attendees=attendees, planner_id=planner_id,
                                   host_id=host_id, rental_items=rental_items, notes=notes, event_id=event_id, error=error)
        set_all_events(name,date,venue_id,start_time,end_time,invitation,image_path,attendees,planner_id,host_id,rental_items,notes)
        return redirect(url_for("show_events", event_id=event_id))
    else:
        venues = database.get_venues()
        hosts = database.get_hosts()
        planners = database.get_planners()
        events=database.get_event(event_id)
        return render_template("event_form.html", events=events, venues=venues, hosts=hosts, planners=planners)
    
@app.route("/events/<event_id>/edit", methods=["GET", "POST"])
def edit_event(event_id=None):
    """This functions serves othe purpose of when a person opens a preexisting it event, they can edit the data within it."""
    matching_event = database.get_event(event_id)
    venues = database.get_venue_and_others(event_id)
    hosts = database.get_host_and_others(event_id)
    planners = database.get_planner_and_others(event_id)
    if request.method == 'POST':
        name = html.escape(request.form['name']),
        date = request.form['date'],
        venue_id = request.form['venue_id'],
        start_time = request.form['start_time'],
        end_time = request.form['end_time'],
        invitation = html.escape(request.form['invitation']),
        image_path = html.escape(request.form['image_path']),
        attendees = request.form['attendees'],
        planner_id =  request.form['planner_id'],
        host_id =  request.form['host_id'],
        rental_items =  html.escape(request.form['rental_items']),
        notes = html.escape(request.form['notes'])
        error=check_events(name,date,venue_id,start_time,end_time,invitation,image_path,attendees,planner_id,host_id,rental_items,notes)
        #error handling is very similar in how add_event is, but rather than referencing set_all_events, database.update event is 
        # referenced.
        if error:
            events=database.get_events(event_id)
            return render_template('event_form.html', name=name, date=date, venue_id=venue_id, 
                                   start_time=start_time, end_time=end_time, invitation=invitation,
                                   image_path=image_path, attendees=attendees, planner_id=planner_id,
                                   host_id=host_id, rental_items=rental_items, notes=notes, event_id=event_id, error=error)
        database.update_event(event_id,name,date,venue_id,start_time,end_time,invitation,image_path,attendees,planner_id,host_id,rental_items,notes)
        return redirect(url_for('show_events', event_id=event_id))
    else:
        #need event=matching_event in order to properly have the preexisting data values show in the form.
        events=database.get_event(event_id)
        return render_template('event_form.html', event=matching_event, events=events, venues=venues, hosts=hosts, planners=planners, action_url=url_for('edit_event', event_id=event_id))
    
@app.route("/events/<event_id>/delete", methods=["GET", "POST"])
def delete_event(event_id=None):
    """This functions serves othe purpose of when a person opens a preexisting it event, they can delete the data as a whole."""
    matching_event = database.get_event(event_id)
    #have to use get method to get data because if the user wants to view the data and not delete then this is neccessary
    if request.method == "GET":
        if matching_event:
            venue=database.get_venue_name_db(event_id)
            host=database.get_host(event_id)
            planner=database.get_planner(event_id)
            return render_template('delete_form.html', event=matching_event, venue=venue,host=host,planner=planner, action_url=url_for('delete_event', event_id=event_id))
    #if the method were just post and not including the get then the delete data would not work properly. that when when they click on the 
    #confirmation the post portion of this function proceeds and the data is removed.
    if request.method == "POST":
        database.delete_event(event_id)
        return redirect(url_for('show_events'))
    
@app.route("/events/<event_id>/attendees/<person_id>/delete", methods=["GET", "POST"])
def delete_attendee(event_id=None, person_id=None):
    if request.method == "GET":
        #I discovered that you must use get method for deleting anything from the database because rather than Posting data, you are removing it.
        database.remove_attendee_event(event_id, person_id)
        return redirect(url_for('show_events', event_id=event_id))
        
@app.route("/events/<event_id>/attendees/add", methods=["GET", "POST"])
def add_attendee(event_id=None):
    if request.method == "POST":
        #since this form requires two primary keys, must have two arguments.
        person_id = request.form['person_id']
        database.add_attendee_event(event_id, person_id)
        return redirect(url_for("show_events", event_id=event_id))
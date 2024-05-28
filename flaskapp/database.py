from pymysql import connect
from pymysql.cursors import DictCursor

from flaskapp.config import DB_HOST, DB_USER, DB_PASS, DB_DATABASE

def get_connection():
    return connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DATABASE,
        cursorclass=DictCursor,
    )

def get_events():
    """Returns a list of dictionaries representing all of the event data"""
    sql = "SELECT * FROM events order by DATE"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            events=cursor.fetchall()
            return events

def get_event(event_id):
    """Takes a event_id, returns a single dictionary containing the data for the event with that id"""
    sql = "SELECT * FROM events WHERE event_id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id,))
            return cursor.fetchone()

def add_event(name,date,venue_id,start_time,end_time,invitation,image_path,attendees,planner_id,host_id,rental_items,notes):
    """Takes as input all of the data for a event. Inserts a new event into the event table"""
    sql = "insert into events (name,date,venue_id,start_time,end_time,invitation,image_path,attendees,planner_id,host_id,rental_items,notes) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name,date,venue_id,start_time,end_time,invitation,image_path,attendees,planner_id,host_id,rental_items,notes))
            conn.commit()

def update_event(event_id, name, date, venue_id, start_time, end_time, invitation, image_path, attendees, planner_id, host_id, rental_items, notes):
    """Takes an event_id and data for an event. Updates the event table with new data for the event with event_id as its primary key"""
    sql = """UPDATE events 
             SET name=%s, date=%s, venue_id=%s, start_time=%s, end_time=%s, invitation=%s, image_path=%s, 
                 attendees=%s, planner_id=%s, host_id=%s, rental_items=%s, notes=%s 
             WHERE event_id=%s"""
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, date, venue_id, start_time, end_time, invitation, image_path,attendees, planner_id, host_id, rental_items, notes, event_id))
            conn.commit()

def delete_event(event_id):
    """Takes an event_id and data for an event. Updates the event table with new data for the event with event_id as its primary key"""
    sql = """DELETE FROM events WHERE event_id = %s"""
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id,))
            conn.commit()

def get_people():
    """Returns a list of dictionaries representing all of the person data"""
    sql = "SELECT * FROM people order by date_of_birth"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            events=cursor.fetchall()
            return events
        
def get_person(person_id):
    sql = "SELECT * FROM people WHERE person_id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (person_id,))
            return cursor.fetchone()

def add_person(name,address,email,date_of_birth,phone,role):
    """Takes as input all of the data for a person and adds a new person to the person table"""
    sql = "INSERT INTO people (name,address,email,date_of_birth,phone,role) VALUES (%s, %s, %s, %s, %s, %s)"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name,address,email,date_of_birth,phone,role))
            conn.commit()

def delete_person(person_id):
    """Takes a person_id and deletes the person with that person_id from the person table"""
    sql = "DELETE FROM people WHERE person_id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (person_id,))
            conn.commit()

def get_attendees(event_id):
    """Returns a list of dictionaries representing all of the data for people attending a particular event"""
    sql = """SELECT e.event_id, p.person_id, p.name, p.address, p.email, p.phone, p.date_of_birth 
    FROM people AS p JOIN event_attendees AS ea ON ea.person_id = p.person_id 
    JOIN events AS e ON e.event_id = ea.event_id WHERE e.event_id = %s"""
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id,))
            attendees=cursor.fetchall()
            return attendees

def add_attendee_event(event_id, person_id):
    """Takes as input a event_id and a attendee_id and inserts the appropriate data into the database that indicates the attendee with attendee_id as a primary key is attending the event with the event_id as a primary key"""
    sql = "insert into event_attendees (event_id, person_id) VALUES (%s, %s)"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id, person_id))
            conn.commit()

def remove_attendee_event(event_id, person_id):
    """Takes as input a event_id and a attendee_id and deletes the data in the database that indicates that the attendee with attendee_id as a primary key
    is attending the event with event_id as a primary key."""
    sql = "DELETE FROM event_attendees where event_id = %s and person_id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id, person_id))
            conn.commit()

def get_customers(event_id):
    sql = """SELECT p.name, p.person_id 
    FROM people AS p
    WHERE p.role = 'customer'
    AND p.person_id NOT IN (
    SELECT ea.person_id
    FROM event_attendees AS ea
    JOIN events AS e ON e.event_id = ea.event_id
    WHERE e.event_id = %s)"""
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id,))
            customer = cursor.fetchall()
            return customer

def get_host(event_id):
    """Takes an event_id and returns the host details for that event"""
    sql = """SELECT e.event_id, e.host_id, p.name, p.email,
    p.phone FROM events AS e JOIN people AS p ON p.person_id = e.host_id WHERE e.event_id = %s"""
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id,))
            host = cursor.fetchone()
            return host
        
def get_host_and_others(event_id):
    """Takes an event_id and returns the host details for that event"""
    sql = """SELECT e.event_id, e.host_id, p.name
        FROM events AS e
        JOIN people AS p ON p.person_id = e.host_id
        WHERE e.event_id = %s

        UNION

        SELECT e2.event_id, e2.host_id, p2.name
        FROM events AS e2
        JOIN people AS p2 ON p2.person_id = e2.host_id
        WHERE e2.event_id <> %s"""
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id, event_id))
            hosts = cursor.fetchall()
            return hosts
        
def get_hosts():
    sql = """SELECT e.event_id, e.host_id, p.name FROM events AS e JOIN people AS p ON
    p.person_id = e.host_id"""
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            hosts = cursor.fetchall()
            return hosts

def set_host(host_id, event_id):
    """Sets the host for the specified event_id"""
    sql = "UPDATE events SET host_id = %s WHERE event_id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (host_id, event_id))
            conn.commit()

def get_planner(event_id):
    """Takes an event_id and returns the planner details for that event"""
    sql = """SELECT e.planner_id, p.name, p.email,
    p.phone FROM events AS e JOIN people AS p ON p.person_id = e.planner_id WHERE e.event_id = %s"""
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id,))
            planner = cursor.fetchone()
            return planner
        
def get_planner_and_others(event_id):
    """Takes an event_id and returns the host details for that event"""
    sql = """SELECT e.event_id, e.planner_id, p.name
        FROM events AS e
        JOIN people AS p ON p.person_id = e.planner_id
        WHERE e.event_id = %s

        UNION

        SELECT e2.event_id, e2.planner_id, p2.name
        FROM events AS e2
        JOIN people AS p2 ON p2.person_id = e2.planner_id
        WHERE e2.event_id <> %s"""
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id, event_id))
            planners = cursor.fetchall()
            return planners
        
def get_planners():
    sql = """SELECT e.event_id, e.planner_id, p.name FROM events AS e JOIN people AS p ON
    p.person_id = e.planner_id"""
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            planners = cursor.fetchall()
            return planners

def set_planner(planner_id, event_id):
    """Sets the planner for the specified event_id"""
    sql = "UPDATE events SET planner_id = %s WHERE event_id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (planner_id, event_id))
            conn.commit()

def get_venues():
    """Returns a list of dictionaries representing all of the venues data"""
    sql = "SELECT * FROM venues order by fee DESC"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            venues=cursor.fetchall()
            return venues
        
def get_venue(venue_id):
    sql = "SELECT * FROM venues WHERE venue_id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (venue_id,))
            return cursor.fetchone()

def get_venue_name_db(event_id):
    sql = """SELECT v.venue_id, e.event_id, v.name FROM venues AS v
    JOIN events AS e ON e.venue_id = v.venue_id 
    WHERE e.event_id = %s"""
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id,))
            return cursor.fetchone()

def get_venue_and_others(event_id):
    """Takes an event_id and returns the host details for that event"""
    sql = """SELECT e.event_id, e.venue_id, v.name
        FROM events AS e
        JOIN venues AS v ON v.venue_id = e.venue_id
        WHERE e.event_id = %s

        UNION

        SELECT e2.event_id, e2.venue_id, v2.name
        FROM events AS e2
        JOIN venues AS v2 ON v2.venue_id = e2.venue_id
        WHERE e2.event_id <> %s"""
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id, event_id))
            planners = cursor.fetchall()
            return planners

def add_venue(name,address,phone,fee,attendees_capacity):
    """Takes as input all of the data for a venue. Inserts a new venue into the event table"""
    sql = "insert into venues (name,address,phone,fee,attendees_capacity) VALUES (%s, %s, %s, %s, %s)"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name,address,phone,fee,attendees_capacity))
            conn.commit()

if __name__ == "__main__":
    # Add test code here to make sure all your functions are working correctly

    print(f"All events: {get_events()}")
    print(f"Event info for event_id 1: {get_event(1)}")
    print(f"All people: {get_people()}")
    print(f"All attendees attending the event with event_id 1: {get_attendees(1)}")

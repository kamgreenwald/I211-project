-- Disable foreign key checks
SET FOREIGN_KEY_CHECKS = 0;

-- Drop all tables
DROP TABLE IF EXISTS venues, people, events, event_attendees;
-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

DROP TABLE IF EXISTS venues;
DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS event_attendees;

CREATE TABLE venues (
venue_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(150),
address VARCHAR(100),
phone VARCHAR(12),
fee INT,
attendees_capacity INT
)ENGINE=INNODB;

CREATE TABLE people (
person_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100),
address VARCHAR(100),
email VARCHAR(100),
date_of_birth DATE,
phone VARCHAR(12),
role ENUM('staff', 'customer')
)ENGINE=INNODB;

CREATE TABLE events (
event_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100),
date DATE,
venue_id INT,
start_time TIME,
end_time TIME,
invitation TEXT,
image_path VARCHAR(30),
attendees INT,
planner_id INT,
host_id INT,
rental_items TEXT,
notes TEXT,
FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
FOREIGN KEY (planner_id) REFERENCES people(person_id),
FOREIGN KEY (host_id) REFERENCES people(person_id)
)ENGINE=INNODB;

CREATE TABLE event_attendees (
event_id INT,
person_id INT,
FOREIGN KEY (event_id) REFERENCES events(event_id),
FOREIGN KEY (person_id) REFERENCES people(person_id)
)ENGINE=INNODB;

INSERT INTO venues (name,address,phone,fee,attendees_capacity) VALUES
("Ruth Chris Steakhouse","123 Main St","317-123-4567",5000,100),
("The Lakeside Pavilion","456 Lake Dr","317-987-6543",3500,200),
("Indianapolis Park","789 Park Ave","317-567-8901",1000,300),
("Butler University Amphitheater","101 University Dr","317-511-2222",1500,2000),
("Riverside Park","321 Park Lane","317-282-3633",2000,1000),
("Caroline's Backyard","12860 Stepping Stone Dr","317-363-4584",1200,75);

INSERT INTO people (name, address, email, date_of_birth, phone, role) VALUES
("Greg Lawrence", "921 W Barouche", "gregoryl@gmail.com", '1965-09-12', "317-987-0987", "customer"),
("Sarah Molina", "789 Oak Ave", "smolina@icloud.com", '1975-08-25', "317-456-2345", "staff"),
("Matt Greenwald", "4545 Kessler Blvd East Dr", "ffmg3@yahoo.com", '1976-08-15', "317-557-2035", "customer"),
("Katie Greenwald", "4545 Kessler Blvd East Dr", "kgreenwald@yahoo.com", '1977-12-06', "317-687-8934", "customer"),
("Megan Kapole", "456 Elm St", "meganK@gmail.com", '1980-04-15', "317-123-7890", "staff"),
("John Carry", "654 Cedar Dr", "johncarry@aol.com", '1982-03-10', "317-458-7890", "staff"),
("Amanda Buskevn", "987 Birch Rd", "amanbusk@gmail.com", '1985-09-15', "317-333-4444", "staff"),
("Michael James", "123 Maple Ln", "michaeljames@yahoo.com", '1987-02-10', "317-567-8901", "staff"),
("David Hoteyn", "101 Pine St", "davidhot@yahoo.com", '1998-06-02', "317-222-1111", "staff"),
("Jacob Kane", "511 W 4th St", "kaneja@gmail.com", '2002-04-30', "317-501-8934", "customer"),
("Caroline Jahanshahi", "11860 Stepping Stone Dr", "carjahan@iu.edu", '2003-01-04', "317-258-9318", "customer");

INSERT INTO events (name, date, venue_id, start_time, end_time, invitation, image_path, attendees, planner_id, host_id, rental_items, notes) VALUES
('Matt and Katie''s Wedding anniversary', '2023-05-01', 1, '5:00', '10:00', 'We would love for you to join us at our third wedding anniversary at 5 p.m. on May 1st, 2023!', 'images/dinner-party.png', 50, 5, 4, 'Tables, Menus, Chairs, Chef, Silverware, Plates, Alcohol', 'Please direct the children to the designated children tables inside the restaurant and the adults to the adults tables.'),
('Jacob''s Graduation Ceremony', '2023-06-02', 2, '2:25', '8:25', 'Celebrate Jacob''s graduation on June 2nd, 2023, at the Butler University Amphitheater!', 'images/graduation-event.png', 1000, 9, 10, 'Stage, Seating, Floral Decor, Graduation Caps, Gowns', 'Please arrive early for the best seats. Parking available in Lot C.'),
('Caroline''s Summer Garden Party', '2023-06-25', 3, '4:00', '12:00', 'Join us for a delightful Summer Garden Party in Caroline''s Backyard on June 25th, 2023!', 'images/outdoor-party.png', 50, 6, 11, 'Tents, Garden Furniture, Outdoor Lighting, Barbecue Grill, Lawn Games, Alcohol', 'Casual attire. Don''t forget your sunglasses and sweatshirts! Please RSVP by June 15th.'),
('Northwind Pharmacuetical''s Annual Picnic', '2023-07-15', 4, '11:00', '4:00', 'Join us for a fun day at the Northwind Pharmacuetical''s annual picnic in City Park on July 15th, 2023!', 'images/picnic.png', 200, 8, 4, 'Picnic Tables, Tents, Grill, Games, Corn Hole, Sound System', 'Please bring your favorite dish to share with your colleagues. Don''t forget sunscreen!'),
('Greg''s 57th Birthday', '2023-08-25', 5, '6:00', '11:00', 'Come celebrate Greg''s 57th birthday with us at The Lakeside Pavilion on August 20th, 2023!', 'images/birthday-party.png', 25, 2, 1, 'Tables, Chairs, DJ, Lighting, Dance Floor, Photo Booth, Cake, Alcohol', 'Please RSVP by August 10th. We look forward to dancing the night away!'),
('Fall Music Festival', '2023-09-15', 6, '12:00', '10:00', 'Get ready for a day of music and fun at Riverside Park''s Fall Music Festival on November 15th, 2023!', 'images/music-concert.png', 750, 7, 10, 'Stage, Sound Equipment, Food Stalls, Portable Toilets, Security', 'No outside food or drinks allowed. Bring your dancing shoes!');

INSERT INTO event_attendees (event_id, person_id) VALUES
(1,3),
(1,4),
(1,5),
(2,10),
(3,11),
(4,10),
(4,11),
(5,1),
(6,3),
(6,4);
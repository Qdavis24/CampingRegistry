INSERT INTO area (name, state, county, city, street_address, zipcode)
VALUES
('Hartman Rocks', 'CO', 'Gunnison', 'Gunnison', '73 Columbine Rd', '81230'),
('Glacier Basin Campground', 'CO', 'Larimer', 'Estes Park', 'Bear Lake Road', '80517'),
('Pinon Flats Campground', 'CO', 'Alamosa', 'Mosca', 'Highway 150', '81146'),
('South Rim Campground', 'CO', 'Montrose', 'Montrose', '9800 Highway 347', '81230'),
('Morefield Campground', 'CO', 'Montezuma', 'Mesa Verde National Park', 'PO Box 8', '81330'),
('Saddlehorn Campground', 'CO', 'Mesa', 'Fruita', 'Rim Rock Drive', '81521'),
('Browns Canyon National Monument', 'CO', 'Chaffee', 'Nathrop', 'County Road 300', '81211'),
('Zapata Falls Campground', 'CO', 'Alamosa', 'Mosca', 'Zapata Falls Road', '81146'),
('Twin Lakes Campground', 'CO', 'Lake', 'Twin Lakes', 'Twin Lakes Road', '81251'),
('Angel of Shavano Campground', 'CO', 'Chaffee', 'Salida', 'County Road 240', '81201'),
('Mueller State Park', 'CO', 'Teller', 'Divide', '21045 Highway 67 South', '80814'),
('Watchman Campground', 'UT', 'Washington', 'Springdale', '1 Zion Park Blvd', '84767'),
('North Campground', 'UT', 'Garfield', 'Bryce', 'P.O Box 640201', '84764'),
('Devils Garden Campground', 'UT', 'Grand', 'Moab', 'PO Box 907', '84532'),
('Fruita Campground', 'UT', 'Wayne', 'Torrey', 'HC 70, Box 15', '84775');


INSERT INTO user (email, first_name, last_name, phone, password, state, city, zipcode, street) 
VALUES
('john.smith@email.com', 'John', 'Smith', '5551234567', 'password', 'CO', 'Gunnison', '81230', '123 Main Street'),
('mary.johnson@email.com', 'Mary', 'Johnson', '5552345678', 'password', 'CA', 'San Diego', '92101', '456 Oak Avenue'),
('pickle.rick@universe.com', 'Pickle', 'Rick', '5558675309', 'password', 'WA', 'Seattle', '98101', '123 Portal Street'),
('robert.williams@email.com', 'Robert', 'Williams', '5553456789', 'password', 'TX', 'Austin', '78701', '789 Elm Boulevard'),
('jennifer.brown@email.com', 'Jennifer', 'Brown', '5554567890', 'password', 'NY', 'Buffalo', '14201', '101 Pine Drive'),
('michael.davis@email.com', 'Michael', 'Davis', '5555678901', 'password', 'FL', 'Miami', '33101', '202 Beach Road'),
('taco.cat@palindrome.org', 'Taco', 'Cat', '5559876543', 'password', 'NM', 'Taos', '87571', '101 Kayak Avenue'),
('sarah.miller@email.com', 'Sarah', 'Miller', '5556789012', 'password', 'IL', 'Chicago', '60601', '303 Lake Street'),
('david.wilson@email.com', 'David', 'Wilson', '5557890123', 'password', 'GA', 'Atlanta', '30301', '404 Peach Lane'),
('lisa.anderson@email.com', 'Lisa', 'Anderson', '5558901234', 'password', 'OR', 'Portland', '97201', '505 Forest Avenue'),
('james.taylor@email.com', 'James', 'Taylor', '5559012345', 'password', 'MA', 'Boston', '02101', '606 Harbor Drive'),
('amanda.white@email.com', 'Amanda', 'White', '5550123456', 'password', 'CO', 'Denver', '80201', '707 Mountain Road'),
('thomas.harris@email.com', 'Thomas', 'Harris', '5551122334', 'password', 'AZ', 'Phoenix', '85001', '808 Desert Trail'),
('jessica.martin@email.com', 'Jessica', 'Martin', '5552233445', 'password', 'OH', 'Columbus', '43201', '909 River Street'),
('william.clark@email.com', 'William', 'Clark', '5553344556', 'password', 'MO', 'St. Louis', '63101', '1010 Arch Avenue');

INSERT INTO site (timestamp, note, electrical, restrooms, shower, nightly_fee, latitude, longitude, area_ID, creator_ID) 
VALUES
('2025/04/15', 'Beautiful mountain vista with easy access to hiking trails. Fire rings available.', 0, 1, 0, 15.00, 38.5492, -107.2495, 1, 1),
('2025/03/15', 'Primitive site next to creek. Very peaceful at night.', 0, 0, 0, 5.00, 37.8298, -106.8687, 2, 2),
('2025/04/18', 'Dense forest coverage with plenty of privacy between sites.', 0, 1, 0, 12.00, 39.1892, -108.2495, 3, 3),
('2025/03/18', 'Desert landscape with gorgeous sunset views.', 0, 0, 0, 8.00, 38.7298, -108.5687, 4, 4),
('2025/04/16', 'Riverside camping with easy water access. Good for kayaking.', 0, 1, 0, 20.00, 39.5492, -106.8495, 5, 5),
('2025/03/17', 'High elevation camping with sweeping valley views.', 0, 0, 0, 0.00, 38.2298, -107.7687, 6, 6),
('2025/04/17', 'Near waterfall with swimming hole. Popular in summer.', 0, 1, 0, 18.00, 37.5492, -107.9495, 7, 7),
('2025/03/19', 'Canyon views with dramatic sunrise colors.', 0, 0, 0, 0.00, 39.0298, -109.2687, 8, 8),
('2025/04/14', 'Lakeside camping with boat launch nearby.', 1, 1, 1, 30.00, 38.9492, -106.5495, 9, 9),
('2025/03/16', 'High alpine meadow. Spectacular wildflowers in season.', 0, 0, 0, 0.00, 37.3298, -106.3687, 10, 10),
('2025/03/14', 'Super cool underground cave, although water fills it during a flash flood', 0, 0, 0, 0.00, -123.4564, 123.3345, 11, 11),
('2025/05/14', 'A nice place built into the side of a hill, I think a hobbit lives here', 0, 0, 0, 10.00, -233.4564, 43.3345, 12, 12),
('2025/04/20', 'Aspen grove with nearby hot springs. Great for fall colors.', 0, 1, 0, 15.00, 38.6789, -107.5432, 13, 13),
('2025/05/01', 'Alpine lake with stunning mountain reflections. Good fishing spot.', 0, 0, 0, 8.00, 39.2345, -106.9876, 14, 14),
('2025/05/01', 'Dungy swamp, not a great place', 0, 0, 0, 0.00, 391.2345, -155.9876, 15, 15);

INSERT INTO liked_user_site (user_ID, site_ID) 
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(11, 11),
(12, 12),
(13, 13),
(14, 14),
(15, 15);

INSERT INTO rule (rule) VALUES
('No campfires during fire bans'),
('Pack out all trash'),
('Quiet hours 10PM-7AM'),
('Pets must be leashed'),
('No washing dishes in bathroom sinks'),
('Respect wildlife - do not feed animals'),
('Maximum stay: 14 days'),
('Park only in designated areas'),
('Children must be supervised'),
('No cutting or damaging trees'),
('Use bear-proof containers where required'),
('Never leave fires unattended'),
('One portable ring to rule them all'),
('Generator hours: 8AM-8PM only'),
('Check out time: 12PM noon');

INSERT INTO site_rule (rule_ID, site_ID) 
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(11, 11),
(13, 12),
(12, 13),
(14, 14),
(15, 15);

INSERT INTO rating (cleanliness, accessibility, quietness, activities, amenities, cost, site_ID) 
VALUES
(6, 7, 8, 5, 6, 7, 1),
(5, 4, 9, 3, 2, 8, 2),
(7, 8, 6, 7, 7, 6, 3),
(6, 5, 8, 4, 3, 7, 4),
(8, 7, 6, 9, 8, 5, 5),
(7, 6, 9, 5, 4, 10, 6),
(8, 7, 7, 8, 7, 6, 7),
(6, 5, 9, 6, 4, 10, 8),
(9, 8, 6, 9, 10, 4, 9),
(7, 6, 10, 7, 5, 10, 10),
(10, 9, 10, 9, 9, 10, 11),
(10, 10, 10, 10, 9, 9, 12),
(8, 7, 8, 7, 6, 7, 13),
(7, 8, 6, 8, 7, 6, 14),
(9, 8, 7, 8, 8, 7, 15);

INSERT INTO photo (filepath, site_ID)
VALUES 
('./static/campsite_photos/camp-photo-1.jpg', 1),
('./static/campsite_photos/camp-photo-2.jpg', 2),
('./static/campsite_photos/camp-photo-3.jpg', 3),
('./static/campsite_photos/camp-photo-4.jpg', 4),
('./static/campsite_photos/camp-photo-5.jpg', 5),
('./static/campsite_photos/camp-photo-6.jpg', 6),
('./static/campsite_photos/camp-photo-7.jpg', 7),
('./static/campsite_photos/camp-photo-8.jpg', 8),
('./static/campsite_photos/camp-photo-9.jpg', 9),
('./static/campsite_photos/camp-photo-10.jpg', 10),
('./static/campsite_photos/camp-photo-11.jpg', 11),
('./static/campsite_photos/camp-photo-12.jpg', 12),
('./static/campsite_photos/camp-photo-13.jpg', 13),
('./static/campsite_photos/camp-photo-14.jpg', 14),
('./static/campsite_photos/camp-photo-15.jpg', 15);

INSERT INTO comment(comment, timestamp, site_ID, user_ID)
VALUES
('Great mountain views and hiking trails. Fire rings were a nice bonus.', '2025/04/20', 1, 1),
('Peaceful creek-side spot. Bring your own toilet paper.', '2025/03/25', 2, 2),
('Good tree cover and privacy between sites.', '2025/04/25', 3, 3),
('Amazing desert sunsets. Basic but worth it.', '2025/03/30', 4, 4),
('Perfect for kayaking with easy river access.', '2025/04/22', 5, 5),
('Incredible valley views and it''s free!', '2025/03/28', 6, 6),
('Nice waterfall and swimming hole. Gets crowded weekends.', '2025/04/23', 7, 7),
('Beautiful canyon sunrise. No cell service.', '2025/03/31', 8, 8),
('Good electrical hookups for our RV. Lake access was convenient.', '2025/04/21', 9, 9),
('Gorgeous wildflowers in the alpine meadow. Cold at night.', '2025/03/27', 10, 10),
('I swear a tiny blue police box appeared then disappeared during the night!', '2025/03/25', 11, 11),
('The hobbit who lives here makes excellent second breakfast.', '2025/04/10', 12, 12),
('Cool cave site. Check weather for flash floods.', '2025/04/15', 13, 13),
('Nice hillside location with good views.', '2025/04/28', 14, 14),
('Aspen trees are beautiful. Hot springs nearby are relaxing.', '2025/05/02', 15, 15);
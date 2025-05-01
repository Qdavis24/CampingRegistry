

DELETE FROM user
WHERE email LIKE "Q%";

SELECT * FROM area;

INSERT INTO area (name, state, county, city, street_address, zipcode)
VALUES
('Yosemite Valley Campground', 'CA', 'Mariposa', 'Yosemite National Park', '9000 Yosemite Valley Rd', '95389'),
('Grand Canyon North Rim Campground', 'AZ', 'Coconino', 'North Rim', '1 North Rim Pkwy', '86023'),
('Acadia Blackwoods Campground', 'ME', 'Hancock', 'Bar Harbor', '21 Eagle Lake Rd', '04609'),
('Great Smoky Mountains Cades Cove', 'TN', 'Blount', 'Townsend', '1 Cades Cove Loop Rd', '37882'),
('Zion South Campground', 'UT', 'Washington', 'Springdale', '1101 Zion Park Blvd', '84767'),
('Rocky Mountain Moraine Park', 'CO', 'Larimer', 'Estes Park', '1000 US-36', '80517'),
('Olympic Hoh Rainforest Campground', 'WA', 'Jefferson', 'Forks', '5000 Upper Hoh Rd', '98331'),
('Yellowstone Grant Village', 'WY', 'Teton', 'Yellowstone National Park', '72 Grant Village Loop', '82190'),
('Everglades Flamingo Campground', 'FL', 'Monroe', 'Homestead', '1 Flamingo Lodge Hwy', '33034'),
('Shenandoah Big Meadows', 'VA', 'Madison', 'Stanley', 'Skyline Dr Mile 51', '22851'),
('Lake Tahoe Emerald Bay', 'CA', 'El Dorado', 'South Lake Tahoe', '138 Emerald Bay Rd', '96150'),
('Crested Butte Mountain', 'CO', 'Gunnison', 'Crested Butte', '12 Gothic Rd', '81224'),
('Adirondack Lake Placid', 'NY', 'Essex', 'Lake Placid', '1932 Olympic Way', '12946'),
('Joshua Tree Hidden Valley', 'CA', 'San Bernardino', 'Twentynine Palms', '74485 National Park Dr', '92277'),
('Glacier National Park Many Glacier', 'MT', 'Glacier', 'Browning', 'Many Glacier Rd', '59417');

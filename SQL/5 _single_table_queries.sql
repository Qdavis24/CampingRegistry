
#1. Select the comment(text) and timestamp from all comments related to a single camp site
SELECT comment, timestamp 
FROM comment 
WHERE site_ID = 1;

#2. Select the filepath from all photos related to a single camp site
SELECT filepath 
FROM photo 
WHERE site_ID = 1;

#3. Select the state, county, street_address, and zipcode for a camping area based on its name
SELECT state, county, street_address, zipcode 
FROM area 
WHERE name = "Hartman Rocks";

#4. Retrieve the names of users located in gunnison
SELECT first_name, last_name
FROM user 
WHERE city = "gunnison";

#5. Retrieve all camping areas that are located in gunnison
SELECT area_ID
FROM area
WHERE city = "gunnison";

#6. Retrieve all the users 

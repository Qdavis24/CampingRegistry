
#1. Select the comment(text) and timestamp from all comments related to a single camp site
SELECT comment, timestamp 
FROM comment 
WHERE site_ID = %s;

#2. Select the filepath from all photos related to a single camp site
SELECT filepath 
FROM photo 
WHERE site_ID = %s;

#3. Select the name, state, county, street_address, and zipcode for the area (camping area) related to a single site
SELECT name, state, county, street_address, zipcode 
FROM area 
WHERE area_ID = %s

#4. Select all columns from user by filtering based on provided email
SELECT * 
FROM user 
WHERE email = %s;
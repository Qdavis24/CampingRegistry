#1. Retrieve all the site IDs for campsites that are in the city of gunnison
SELECT s.site_ID
FROM site as s
JOIN area as a 
ON s.area_ID = a.area_ID
WHERE a.city LIKE "%gunnison%"
LIMIT 5;

#2. Retrieve all of the site IDs that belong to hartman rocks camping area
SELECT s.site_ID
FROM site as s
JOIN area as a ON s.site_ID = a.site_ID
WHERE a.name = "Hartman Rocks";

#3. Find the top 5 highest-rated camping sites based on average overall rating
SELECT s.site_ID, AVG(r.cleanliness + r.accessibility + r.quietness + r.activities +  r.amenities + r.cost) as overall_score
FROM site as s
JOIN rating as r ON s.site_ID = r.site_ID
GROUP BY s.site_ID
ORDER BY overall_score DESC
LIMIT 5;

#4. Find the top 5 rated sites based on average rating for a single category
SELECT s.site_ID, AVG(r.cleanliness) as cleanliness_score
FROM site as s
JOIN rating as r ON s.site_ID = r.site_ID
GROUP BY s.site_ID
ORDER BY cleanliness_score DESC
LIMIT 5;

#5. Find the average overall rating for a site
SELECT AVG(r.cleanliness + r.accessibility + r.quietness + r.activities +  r.amenities + r.cost)/6 as avg
FROM site as s
JOIN rating as r
ON s.site_ID = r.site_ID
WHERE s.site_ID = 1;

#6. Find the average rating for a single category for a site
SELECT AVG(r.cleanliness)
FROM site as s
JOIN rating as r ON s.site_ID = r.site_ID
WHERE s.site_ID = 1;

#7. Find all the rules related to a single site
SELECT r.rule
FROM rule as r 
JOIN site_rule as sr ON r.rule_ID = sr.rule_ID 
JOIN site as s ON s.site_ID = sr.site_ID
WHERE sr.site_ID = 1;

#7. Retrieve all photo filepaths for campsites in a specific camping area
SELECT p.filepath
FROM site as s
JOIN photo as p
ON s.site_ID = p.site_ID
JOIN area as a 
ON s.area_ID = a.area_ID
WHERE a.name = "Hartman Rocks";


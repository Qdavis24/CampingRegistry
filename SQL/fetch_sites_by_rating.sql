# get rules comments, photo, and rating, for a site

# filter site by rating

DELIMITER $$
DROP PROCEDURE IF EXISTS fetch_sites_by_rating;
CREATE PROCEDURE fetch_sites_by_rating(


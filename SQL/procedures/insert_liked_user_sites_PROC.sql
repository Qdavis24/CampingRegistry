## write a query for inserting data into saved user site that will confirm the site being saved is not created by user

DROP PROCEDURE IF EXISTS insert_liked_user_sites;
DELIMITER $$
CREATE PROCEDURE insert_liked_user_sites(IN user_ID INT, IN site_ID INT)
BEGIN

IF (SELECT creator_ID FROM site WHERE site.site_ID = site_ID) != user_ID THEN
INSERT INTO liked_user_site
VALUE(user_ID, site_ID);
END IF;


END $$

DELIMITER ;
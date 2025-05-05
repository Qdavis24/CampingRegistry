DROP PROCEDURE IF EXISTS fetch_liked_user_sites;
DELIMITER $$
CREATE PROCEDURE fetch_liked_user_sites(IN ID INT)
BEGIN
SELECT site.site_ID
FROM site
JOIN liked_user_site
ON site.site_ID = liked_user_site.site_ID
JOIN user
ON user.user_ID = liked_user_site.user_ID
WHERE user.user_ID = ID;
END$$
DELIMITER ;



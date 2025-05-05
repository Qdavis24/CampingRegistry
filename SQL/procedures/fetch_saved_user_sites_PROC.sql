DELIMITER $$
DROP PROCEDURE IF EXISTS fetch_user_saved_sites;
CREATE PROCEDURE fetch_user_saved_sites(IN ID INT)
BEGIN

SELECT *
FROM site
JOIN saved_user_site
ON site.site_ID = saved_user_site.site_ID
JOIN user
ON user.user_ID = saved_user_site.user_ID
WHERE user.user_ID = ID;

END$$
DELIMITER ;



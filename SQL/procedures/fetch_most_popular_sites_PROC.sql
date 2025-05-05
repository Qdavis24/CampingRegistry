DROP PROCEDURE IF EXISTS fetch_most_popular_sites;
DELIMITER $$
CREATE PROCEDURE fetch_most_popular_sites(IN num INT)
BEGIN
SELECT s.site_ID, AVG(r.cleanliness + r.accessibility + r.quietness + r.activities +  r.amenities + r.cost) as overall_score
FROM site as s
JOIN rating as r ON s.site_ID = r.site_ID
GROUP BY s.site_ID
ORDER BY overall_score DESC
LIMIT num;
END$$
DELIMITER ;
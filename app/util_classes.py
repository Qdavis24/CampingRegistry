from flask_wtf import FlaskForm
from flask_login import UserMixin
from .exceptions import LimitError
import logging


class FormHandler:
    def __init__(self, flask_form: FlaskForm):
        self.form: FlaskForm = flask_form
        self.fields: list = self.to_list()
        self.break_point: int = len(self.fields)//2
    def to_list(self):
        fields: list = [field for field in self.form if field.name not in ["csrf_token", "submit"]]
        return fields

class User(UserMixin):
    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.id = self.user_ID

class CampsitesManager:
    def __init__(self):
        self.highest_rated_by_overall = []
        self.highest_rated_by_cleanliness = []
        self.highest_rated_by_accessibility = []
        self.highest_rated_by_quietness = []
        self.highest_rated_by_activities = []
        self.highest_rated_by_ammenities = []
        self.highest_rated_by_cost = []

        self.area_map = {}
    
        
    def fetch_by_areas(self, app, search_type, search_term, offset, limit):
        if limit < 1:
            raise LimitError()
        if offset < 0:
            raise LimitError()
        
        site_ids = None
        with app.retrieve_db_connection() as (connection, cursor):
            try:
                cursor.execute(f"""SELECT s.*
                                  FROM site as s
                                  JOIN area as a 
                                  ON s.area_ID = a.area_ID
                                  WHERE a.{search_type} LIKE %s
                                  LIMIT 1 OFFSET %s""", (search_term,offset))
            except Exception as e:
                logging.error(f"failure to retrieve sites from location type and name : {e}")
            else:
                site_ids = [row["site_ID"] for row in cursor.fetchall()]

        return site_ids
    def fetch_by_area(self, app, area_id, offset, limit):
        """ Fetches the campsite IDs for a given area ID.
        Args:
            app: The Flask app instance.
            area_id: The ID of the area to fetch campsite IDs for.
            limit: The maximum number of campsite IDs to fetch. (must be sanitized for sql injection)
        Returns:
            A list of campsite IDs for the given area ID.
        Raises:
            LimitError: If the limit is less than 1.
        """
        if limit < 1:
            raise LimitError("Limit must be greater than 0")
        if offset < 0:
            raise LimitError("Offset must be greater than or equal to 0")
        if area_id in self.area_map and len(self.area_map[area_id]) >= limit+offset:
            return self.area_map[area_id][offset:limit+offset]
        with app.retrieve_db_connection() as (connection, cursor):
            try:
                cursor.execute("""SELECT s.site_ID
                                    FROM site as s
                                    JOIN area as a ON s.site_ID = a.site_ID
                                    WHERE a.area_ID = %s
                                    LIMIT %s OFFSET %s;""", (area_id, limit, offset))
            except Exception as e:
                logging.error(f"ERROR fetching area data: {e}")
            else:
                area_campsite_ids = [row["site_ID"] for row in cursor.fetchall()]
                if area_id not in self.area_map:
                    self.area_map[area_id] = []
                if len(self.area_map[area_id]) == offset:
                    self.area_map[area_id].extend(area_campsite_ids)
        return area_campsite_ids or None
    
    def fetch_by_overall_rating(self, app, limit):
        """ Fetches the highest rated campsites by overall rating.
        Args: 
            app: The Flask app instance.
            limit: The number of top-rated campsites to fetch.
        Returns:
            A list of campsite IDs for the highest rated campsites. 
        Raises:
            LimitError: If the limit is less than 1.
        """
        if limit < 1:
            raise LimitError("Limit must be greater than 0")
        if len(self.highest_rated_by_overall) >= limit:
            return self.highest_rated_by_overall[:limit]
        overall_rated_site_ids = None
        with app.retrieve_db_connection() as (connection, cursor):
            try:
                cursor.execute("""SELECT s.site_ID, AVG(r.cleanliness + r.accessibility + r.quietness + r.activities +  r.amenities + r.cost) as overall_score
                                    FROM site as s
                                    JOIN rating as r ON s.site_ID = r.site_ID
                                    GROUP BY s.site_ID
                                    ORDER BY overall_score DESC
                                    LIMIT %s;""", (limit,))
            except Exception as e:
                logging.error(f"ERROR fetching overall rating data: {e}")
            else:
                overall_rated_site_ids = [row["site_ID"] for row in cursor.fetchall()]
                self.highest_rated_by_overall.extend(overall_rated_site_ids[len(self.highest_rated_by_overall):])
        return overall_rated_site_ids
    
    def fetch_by_category_rating(self, app, category, limit):
        """ Fetches the highest rated campsites by a specific category.
        Args:
            app: The Flask app instance.
            category: The category to fetch ratings for. Must be one of the RATING_CATEGORIES. (requires sanitation for sql injection)
            limit: The number of top-rated campsites to fetch. (must be sanitized for sql injection)
        Returns:
            A list of campsite IDs for the highest rated campsites in the specified category.
        Raises:
            LimitError: If the limit is less than 1.
            ValueError: If the category is not valid.
        """
        if category not in Campsite.RATING_CATEGORIES:
            logging.error(f"Invalid rating category: {category}")
            raise ValueError(f"Invalid rating category: {category}")
        if limit < 1:
            raise LimitError("Limit must be greater than 0")
        if len(getattr(self, f"highest_rated_by_{category}")) >= limit:
            return getattr(self, f"highest_rated_by_{category}")[:limit]
        
        with app.retrieve_db_connection() as (connection, cursor):
            try:
                cursor.execute(f"""SELECT s.site_ID, AVG(r.{category}) as {category}_score
                                    FROM site as s
                                    JOIN rating as r ON s.site_ID = r.site_ID
                                    GROUP BY s.site_ID
                                    ORDER BY {category}_score DESC
                                    LIMIT %s;""", (limit,))
            except Exception as e:
                logging.error(f"ERROR fetching {category} rating data: {e}")
            else:
                category_rated_site_ids = [row["site_ID"] for row in cursor.fetchall()]
                new_category_rated_site_ids = getattr(self, f"highest_rated_by_{category}")
                new_category_rated_site_ids.extend(category_rated_site_ids[len(new_category_rated_site_ids):])
                setattr(self, f"highest_rated_by_{category}", new_category_rated_site_ids)
        return category_rated_site_ids or None


class Campsite:
    """ the fetch data method will return non formatted data directly from sql queries
        that looks like this - come up with a standaradized approach to formatting after finishing mvp
        currently only serialize method will handle this along with hacky constructor format
        [
        {'ratings': 
            {
                'overall': [{'avg': Decimal('9.00000000')}],
                'cleanliness': [{'AVG(r.cleanliness)': Decimal('9.2000')}],
                'accessibility': [{'AVG(r.accessibility)': Decimal('8.6000')}],
                'quietness': [{'AVG(r.quietness)': Decimal('9.8000')}],
                'activities': [{'AVG(r.activities)': Decimal('9.2000')}],
                'amenities': [{'AVG(r.amenities)': Decimal('8.4000')}],
                'cost': [{'AVG(r.cost)': Decimal('8.8000')}]
            },
            'comments': [],
            'rules': [],
            'filepaths': ['./static/campsite_photos/template.jfif'],
            'area': [
                {
                    'name': 'Yosemite Valley Campground',
                    'state': 'CA',
                    'county': 'Mariposa',
                    'street_address': '9000 Yosemite Valley Rd',
                    'zipcode': '95389'
                }
            ]
            }
                """
    RATING_CATEGORIES = ("cleanliness", "accessibility", "quietness", "activities", "amenities", "cost")
    def __init__(self, app, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.overall_score = None
        self.cleanliness_score = None
        self.accessibility_score = None
        self.quietness_score = None
        self.activities_score = None
        self.amenities_score = None
        self.cost_score = None
        self.comments: list = None
        self.rules: list = None 
        self.filepaths: list = None
        self.area: dict = None
        
        self._fetch_related_data(app)

        self.rating_categories = {
            "overall_score" : self.overall_score,
            "cleanliness_score" : self.cleanliness_score,
            "accessibility_score" : self.accessibility_score,
            "quietness_score": self.quietness_score,
            "activities_score" : self.activities_score,
            "amenities_score" : self.amenities_score,
            "cost_score": self.cost_score
        }
        self._clean_rating_scores()
        if self.filepaths:
            self.filepaths = [row["filepath"] for row in self.filepaths]
        if self.area:
            self.area = self.area[0]
        if self.rules:
            self.rules = [row["rule"] for row in self.rules] if len(self.rules) > 0 else []
       
    def serialize(self):
        rating_category_scores = {
            "overall": self.overall_score,
            "cleanliness": self.cleanliness_score,
            "accessibility": self.accessibility_score,
            "quietness": self.quietness_score,
            "activities": self.activities_score,
            "amenities": self.amenities_score,
            "cost": self.cost_score
        }
        serialized_data = {
            "site_ID": self.site_ID,
            "ratings" : rating_category_scores,
            "comments" : self.comments,
            "rules" : self.rules,
            "filepaths" : self.filepaths,
            "area": self.area
        }
        return serialized_data
    
    def _clean_rating_scores(self):
        for attr, rating in self.rating_categories.items():
            if list(rating[0].values())[0]:
                cleaned_number = float(list(rating[0].values())[0])
                setattr(self, attr, cleaned_number)
            else:
                setattr(self, attr, None)
            

    def _fetch_related_data(self, app):
        queries = {
            "overall_score": (self.site_ID, """SELECT AVG(r.cleanliness + r.accessibility + r.quietness + r.activities +  r.amenities + r.cost)/6 as avg
                                 FROM site as s
                                 JOIN rating as r
                                 ON s.site_ID = r.site_ID
                                 WHERE s.site_ID = %s;"""),

            "cleanliness_score": (self.site_ID, """SELECT AVG(r.cleanliness)
                                    FROM site as s
                                    JOIN rating as r ON s.site_ID = r.site_ID
                                    WHERE s.site_ID = %s;"""),

            "accessibility_score": (self.site_ID, """SELECT AVG(r.accessibility)
                                       FROM site as s
                                       JOIN rating as r ON s.site_ID = r.site_ID
                                       WHERE s.site_ID = %s;"""),

            "quietness_score": (self.site_ID, """SELECT AVG(r.quietness)
                                    FROM site as s
                                    JOIN rating as r ON s.site_ID = r.site_ID
                                    WHERE s.site_ID = %s;"""),

            "activities_score": (self.site_ID, """SELECT AVG(r.activities)
                                    FROM site as s
                                    JOIN rating as r ON s.site_ID = r.site_ID
                                    WHERE s.site_ID = %s;"""),

            "amenities_score": (self.site_ID, """SELECT AVG(r.amenities)
                                    FROM site as s
                                    JOIN rating as r ON s.site_ID = r.site_ID
                                    WHERE s.site_ID = %s;"""),

            "cost_score": (self.site_ID, """SELECT AVG(r.cost)
                                    FROM site as s
                                    JOIN rating as r ON s.site_ID = r.site_ID
                                    WHERE s.site_ID = %s;"""),

            "comments" : (self.site_ID, """SELECT comment, timestamp 
                            FROM comment 
                            WHERE site_ID = %s;"""),

            "filepaths" : (self.site_ID, """SELECT filepath 
                             FROM photo 
                             WHERE site_ID = %s;"""),

            "rules": (self.site_ID, """SELECT r.rule
                        FROM rule as r 
                        JOIN site_rule as sr ON r.rule_ID = sr.rule_ID 
                        JOIN site as s ON s.site_ID = sr.site_ID
                        WHERE sr.site_ID = %s;"""),

            "area" : (self.area_ID, """SELECT name, state, county, city, street_address, zipcode 
                        FROM area 
                        WHERE area_ID = %s""")
        }
        with app.retrieve_db_connection() as (connection, cursor):
            for attr, query in queries.items():
                try:
                    cursor.execute(query[1], (query[0],))
                except Exception as e:
                    logging.error(f"ERROR fetching {attr} for campsite {self.site_ID}: {e}")
                else:
                    setattr(self, attr, cursor.fetchall())


    
    
        
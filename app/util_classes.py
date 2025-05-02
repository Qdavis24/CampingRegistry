from flask_wtf import FlaskForm
from flask_login import UserMixin
from .exceptions import LimitError


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
    def __init__(self, app, raw_campsites_data):
        self.campsites = []
        self._process_raw_campsites_data(app, raw_campsites_data)
    def _process_raw_campsites_data(self, app, raw_campsites_data):
        for raw_campsite_data in raw_campsites_data:
            new_campsite = Campsite(app, **raw_campsite_data)
            self.campsites.append(new_campsite)
    def get_highest_rated(self, rating_category, limit):
        """ categories are as follows
        "cleanliness", "accessibility", "quietness", "activities", "amenities", "cost", "overall"
        limit will allow you specify how many to return
        """
        if len(self.campsites) < limit:
            raise LimitError
        elif len(self.campsites) == limit:
            return self.campsites.copy()
        
        return sorted(self.campsites, key=lambda campsite: campsite.rating_category_scores[rating_category])[-limit:]
            


class Campsite:
    RATING_CATEGORIES = ("cleanliness", "accessibility", "quietness", "activities", "amenities", "cost")
    def __init__(self, app, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.ratings: list = None 
        self.comments: list = None
        self.rules: list = None 
        self.filepaths: list = None
        self.area: dict = None

        self._fetch_related_data(app)

        if self.ratings and len(self.ratings) > 0:
            self.rating_category_scores: dict = {cat: self._get_rating_category_score(cat) for cat in Campsite.RATING_CATEGORIES}
            self._get_overall_score()

        

    def _fetch_related_data(self, app):
        queries = {
            "ratings" : "SELECT cleanliness, accessibility, quietness, activities, amenities, cost FROM rating WHERE site_ID = %s;",
            "comments" : "SELECT comment, timestamp FROM comment WHERE site_ID = %s;",
            "filepaths" : "SELECT filepath FROM photo WHERE site_ID = %s;",
            "rules": "SELECT r.rule FROM rule as r JOIN siterule as sr ON r.rule_ID = sr.rule_ID join site as s ON s.site_ID = sr.site_ID WHERE sr.site_ID = %s;",
            "area" : "SELECT name, state, county, street_address, zipcode FROM area WHERE site_ID = %s"
        }
        with app.retrieve_db_connection() as (connection, cursor):
            for attr, query in queries.items():
                try:
                    cursor.execute(query, (self.site_ID,))
                except Exception as e:
                    logging.error(f"ERROR fetching {attr} for campsite {self.site_ID}: {e}")
                else:
                    setattr(self, attr, cursor.fetchall())

    def _get_overall_score(self):
        sum_score = 0
        for cat, score in self.rating_category_scores.items():
            sum_score += score
        self.rating_category_scores["overall"] = sum_score / len(Campsite.RATING_CATEGORIES)
        

    def _get_rating_category_score(self, category):
        sum_score = 0
        for rating in self.ratings:
            sum_score += rating[category]
        return sum_score / len(self.ratings)

    
    
        
from flask_wtf import FlaskForm
from flask_login import UserMixin

class FormHandler:
    def __init__(self, flask_form: FlaskForm):
        self.form: FlaskForm = flask_form
        self.fields: list = self.to_list()
        self.break_point: int = len(self.fields)//2
    def to_list(self):
        fields: list = [field for field in self.form if field.name not in ["csrf_token", "submit"]]
        return fields

class User(UserMixin):
    def __init__(self, id, **kwargs):
        super().__init__()
        self.id = id
        for key, value in kwargs:
            self.key = value
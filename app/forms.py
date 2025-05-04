from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired, Length, ValidationError, Regexp, NumberRange
import logging

# region auth forms
class RegisterForm(FlaskForm):
    email: EmailField = EmailField(
        label="Email", validators=[DataRequired(), Length(min=5, max=50)]
    )
    first_name: StringField = StringField(
        label="First Name", validators=[DataRequired(), Length(max=30)]
    )
    last_name: StringField = StringField(
        label="Last Name", validators=[DataRequired(), Length(max=30)]
    )
    state: StringField = StringField(
        label="State (CO)"
    )
    city: StringField = StringField(
        label="City", validators=[DataRequired(), Length(max=50)]
    )
    phone: StringField = StringField(
        label="Phone Number",
        validators=[
            DataRequired(),
            Length(min=10, max=10),
            Regexp(r"^\d{10}$", message="Phone number must be valid."),
        ],
    )
    state: StringField = StringField(
        label="State", validators=[DataRequired(), Length(min=2, max=2)])
    city: StringField = StringField(
        label="City", validators=[DataRequired(), Length(min=4, max=40)]
    )
    zipcode: StringField = StringField(label="5 digit zipcode",
                                       validators=[DataRequired(), Length(min=5, max=5)])
    street: StringField = StringField(label="Street address", 
                                      validators=[DataRequired(), Length(min=4, max=40)])
    password: PasswordField = PasswordField(
        label="Password", validators=[DataRequired(), Length(min=4, max=64)]
    )
    password_check: PasswordField = PasswordField(
        label="Re-enter Password", validators=[DataRequired(), Length(min=4,max=64)]
    )
    submit = SubmitField()

    def validate_email(self, email):
        if "@" not in email.data or ".com" not in email.data:
            raise ValidationError("Email must be valid email address.")

class LoginForm(FlaskForm):

    email: EmailField = EmailField(
        label="email", validators=[DataRequired(), Length(min=5, max=50)]
    )
    password: PasswordField = PasswordField(
        label="password", validators=[DataRequired(), Length(min=4,max=64)]
    )
    submit = SubmitField()

    def validate_email(self, email):
        if "@" not in email.data or ".com" not in email.data:
            raise ValidationError("Email must be valid email address.")
# endregion

class CreatSiteForm(FlaskForm):
    area = SelectField('Area', validators=[DataRequired()], coerce=int)
    note = TextAreaField('Note')
    nightly_fee = DecimalField('Fee', validators=[DataRequired()], places=2)
    electrical = BooleanField('Electrical')
    restrooms = BooleanField('Restrooms')
    shower = BooleanField('Shower')
    photos = MultipleFileField(label="Photos")
    latitude = DecimalField("Latitude", validators=[DataRequired()], places=7)
    longitude = DecimalField("Longitude", validators=[DataRequired()], places=7)
    submit = SubmitField('Create Site')
    
    def __init__(self, app, *args, **kwargs):
        super(CreatSiteForm, self).__init__(*args, **kwargs)
        self.populate_area_choices(app)
    
    def populate_area_choices(self, app):
        """Populate area choices from database"""
        choices = []
        try:
            with app.retrieve_db_connection() as (connection, cursor):
                cursor.execute("SELECT area_ID, name FROM area;")
                choices = [(row["area_ID"], row["name"]) for row in cursor.fetchall()]
        except Exception as e:
            logging.error(f"Failure to retrieve areas for create site form: {e}")
        
        self.area.choices = choices

class RatingSiteForm(FlaskForm):
    cleanliness_rating = SelectField('Cleanliness Rating', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], validators=[DataRequired()])
    accessibility_rating = SelectField('Accessibility Rating', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], validators=[DataRequired()])
    quietness_rating = SelectField('Quietness Rating', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], validators=[DataRequired()])
    activities_rating = SelectField('Activites Rating', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], validators=[DataRequired()])
    amenities_rating = SelectField('Amenities Rating', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], validators=[DataRequired()])
    cost_rating = SelectField('Cost Rating', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], validators=[DataRequired()])
   
    submit = SubmitField()

class CommentSiteForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=1, max=250)])
    submit = SubmitField()
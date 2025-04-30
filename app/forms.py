from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Regexp


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

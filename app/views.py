from .forms import LoginForm, RegisterForm
from .util_classes import FormHandler
from flask_login import login_user, login_required, current_user
from flask import render_template, url_for, Blueprint, redirect, current_app, flash
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import MySQLConnection
import logging



app_blueprint = Blueprint("app_blueprint", "app_blueprint")


@app_blueprint.route("/", methods=["GET"])
def index(register_form=None, login_form=None):
    register_form: RegisterForm = register_form or RegisterForm()
    register_form_handler: FormHandler = FormHandler(register_form)
    login_form: LoginForm = login_form or LoginForm()
    login_form_handler: FormHandler = FormHandler(login_form)
    return render_template(
        "index.html",
        register_form=register_form,
        register_form_handler=register_form_handler,
        login_form=login_form,
        login_form_handler=login_form_handler
    )


@app_blueprint.route("/register", methods=["POST"])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        first_name = register_form.first_name.data
        last_name = register_form.last_name.data
        phone = register_form.phone.data
        email = register_form.email.data
        password = register_form.password.data
        state = register_form.state.data 
        city = register_form.city.data
        zipcode = register_form.zipcode.data
        street = register_form.street.data
        hashed_password = generate_password_hash(password)

        value = (first_name, last_name, phone, email, hashed_password, state, city, zipcode, street)
        
        with current_app.retrieve_db_connection() as (connection, cursor):
            try:
                cursor.execute("" \
                "INSERT INTO user (first_name, last_name, phone, email, password, state, city, zipcode, street)" \
                "VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s)", value)
            except Exception as e:
                logging.error(e)
                connection.rollback()
            else:
                connection.commit()
                login_user(cursor.lastrowid)

        return redirect(url_for("app_blueprint.areas"))
    
    return redirect(url_for("app_blueprint.index", register_form=register_form))

@app_blueprint.route("/login", methods=["POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        with current_app.retrieve_db_connection() as (connection, cursor):
            try:
                cursor.execute("SELECT * FROM user WHERE email = %s;", (email,))
            except Exception as e:
                logging.error(e)
            else:
                user = cursor.fetchone()
                if not user:
                    flash("Email entered does not exists.")
                    return redirect(url_for("app_blueprint.index"))
                if (check_password_hash(password=password, pwhash=user["password"])):
                    login_user(user["user_ID"])
                    
            
        return redirect(url_for("app_blueprint.areas"))
    return redirect(url_for("app_blueprint.index", login_form=login_form))

@login_required
@app_blueprint.route("/areas", methods=["GET"])
def areas():
    with current_app.retrieve_db_connection() as (connection, cursor):
        try:
            cursor.execute("SELECT * FROM area;")
            areas = cursor.fetchall()
            print(areas)
        except Exception as e:
            logging.error(e)
    return render_template("areas.html", areas=areas)
    

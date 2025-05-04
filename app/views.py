from .forms import LoginForm, RegisterForm, CreatSiteForm
from .util_classes import FormHandler, CampsitesManager, User, Campsite
from .exceptions import LimitError
from flask_login import login_user, login_required, current_user, logout_user
from flask import render_template, url_for, Blueprint, redirect, current_app, flash, session, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import MySQLConnection
import logging
import uuid
import os



app_blueprint = Blueprint("app_blueprint", "app_blueprint")

campsite_manager = CampsitesManager()

UPLOAD_PATH = "./static/campsite_photos"

def save_files(files):
    uploaded_files = files
    saved_file_paths = []
    
    if uploaded_files:
        # Ensure directory exists
        os.makedirs(UPLOAD_PATH, exist_ok=True)
        
        for file in uploaded_files:
            if file.filename:
                # Generate a unique filename using UUID
                original_ext = os.path.splitext(file.filename)[1]
                unique_filename = f"{uuid.uuid4()}{original_ext}"
                
                # Create full filepath
                file_path = os.path.join(UPLOAD_PATH, unique_filename)
                
                # Save the file
                file.save(file_path)
                saved_file_paths.append(file_path)
    
    return saved_file_paths


@app_blueprint.route("/", methods=["GET", "POST"])
def index(curr_modal=None):
    # auth forms setup
    register_form: RegisterForm = session.pop("register_form", None) or RegisterForm()
    register_form_handler: FormHandler = FormHandler(register_form)

    login_form: LoginForm = session.pop("login_form", None) or LoginForm()
    login_form_handler: FormHandler = FormHandler(login_form)

    create_site_form: CreatSiteForm = session.pop("create_site_form", None) or CreatSiteForm(current_app)

    
    # campsite retrieval
    highest_rated_campsites_by_overall: list = None
    highest_rated_campsites_by_overall_raw: list = None
    highest_rated_campsites_by_overall_ids: list = campsite_manager.fetch_by_overall_rating(current_app, limit=5)
    
    user_created_campsites: list = None
    user_created_campsites_raw: list = None

    with current_app.retrieve_db_connection() as (connection, cursor):
        if current_user:
            try:
                cursor.execute("SELECT * FROM site WHERE creator_ID = %s LIMIT 5", (current_user.id,))
            except Exception as e:
                logging.error(f"failure to retrieve current user's created sites : {e}")
            else:
                user_created_campsites_raw = cursor.fetchall()

        if highest_rated_campsites_by_overall_ids:
            try:
                cursor.execute(f"SELECT * FROM site WHERE site_ID in {tuple(highest_rated_campsites_by_overall_ids)}")
            except Exception as e:
                logging.error(f"Failure to load sites from highest rated sites: {e}")
            else:
                highest_rated_campsites_by_overall_raw = cursor.fetchall()

        if highest_rated_campsites_by_overall_raw:
            highest_rated_campsites_by_overall = CampsitesManager.process_raw_campsites(current_app, highest_rated_campsites_by_overall_raw)
        if user_created_campsites_raw:
            user_created_campsites = CampsitesManager.process_raw_campsites(current_app, user_created_campsites_raw)

    return render_template(
        "index.html",
        register_form=register_form,
        register_form_handler=register_form_handler,
        login_form=login_form,
        login_form_handler=login_form_handler,
        create_site_form=create_site_form,
        highest_rated_campsites_by_overall=highest_rated_campsites_by_overall,
        user_created_campsites=user_created_campsites,
        curr_modal=curr_modal
    )

#region auth

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

        return redirect(url_for("app_blueprint.index"))
    session["register_form"] = register_form
    return redirect(url_for("app_blueprint.index", curr_modal="register-modal"))

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
                logging.error(f"ERROR login database query : {e}")
            else:
                user = cursor.fetchone()
                if not user:
                    flash("Email entered does not exists.")
                    return redirect(url_for("app_blueprint.index"))
                if (check_password_hash(password=password, pwhash=user["password"])):
                    login_user(User(**user))
                    
            
        return redirect(url_for("app_blueprint.index"))
    session["login_form"] = login_form
    return redirect(url_for("app_blueprint.index", curr_modal="login-modal"))

@login_required
@app_blueprint.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("app_blueprint.index"))
    
#endregion

@login_required
@app_blueprint.route("/create", methods=["GET", "POST"])
def create():
    create_site_form = CreatSiteForm(current_app)
    if create_site_form.validate_on_submit():
        area_ID: int = create_site_form.area.data
        note: str = create_site_form.note.data
        electrical: bool = create_site_form.electrical.data
        restrooms: bool = create_site_form.restrooms.data
        shower: bool = create_site_form.shower.data
        nightly_fee: float = create_site_form.nightly_fee.data
        latitude: float = create_site_form.latitude.data
        longitude: float = create_site_form.longitude.data

        with current_app.retrieve_db_connection() as (connection, cursor):
            try:
                try:
                    cursor.execute("""INSERT INTO site (timestamp, note, electrical, restrooms, shower, nightly_fee, latitude, longitude, area_ID, creator_ID)
                                    VALUES (CURRENT_DATE(), %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                    (note, electrical, restrooms, shower, nightly_fee, latitude, longitude, area_ID, current_user.id))
                except Exception as e:
                    logging.error(f"failure to insert new site : {e}")
                else:
                    site_ID = cursor.lastrowid
                
                filepaths = save_files(create_site_form.photos.data)

                if filepaths:
                    for filepath in filepaths:
                        try:
                            cursor.execute("""INSERT INTO photo (filepath, site_ID)
                                            VALUES(%s, %s)""", (filepath, site_ID))
                        except Exception as e:
                            logging.error(f"failure to insert filepath {filepath} : {e}")
            except Exception as e:
                flash("Site failed to save")
                connection.rollback()
                logging.error(f"failure to upload site : {e} - rolling back queries")
            else:
                connection.commit()        
        return redirect(url_for("app_blueprint.index"))
    session["create_site_form"] = create_site_form
    return redirect(url_for("app_blueprint.index", curr_modal="create-site-modal"))
                    
                
@app_blueprint.route("/search-by-location", methods=["GET"])
def search_by_location():
    search_type = request.args.get("search-type")
    search_term = f"%{request.args.get('search-term')}%"

    site_ids = campsite_manager.fetch_by_areas(current_app, search_type, search_term, 9)

    if (len(site_ids) < 1):
        return jsonify({
            "status": 200,
            "count": 0,
            "message": f"No site found under {search_type} {search_term}",
            "campsites": [],
            "success": True
        })

    sites = None
    print(site_ids)
    with current_app.retrieve_db_connection() as (connection, cursor):
        try:
            cursor.execute(f"SELECT * FROM site WHERE site_ID IN {tuple(site_ids)}")
        except Exception as e:
            logging.error(f"failure to retrieve site by location type and name from site : {e}")
        else:
            sites = [Campsite(current_app, **row) for row in cursor.fetchall()]

    return jsonify({
            "status": 200,
            "count": 0,
            "message": "Sites found",
            "campsites": sites,
            "success": True
        })



        

    
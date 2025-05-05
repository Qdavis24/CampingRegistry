from .forms import LoginForm, RegisterForm, CreateSiteForm, RatingSiteForm, CommentSiteForm
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

from werkzeug.utils import secure_filename
import os
import uuid

# Define an absolute path for clarity
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_PATH = os.path.join(BASE_DIR, "static", "campsite_photos")

def save_files(files):
    uploaded_files = files
    saved_file_paths = []
    
    if uploaded_files:
        # Ensure directory exists
        os.makedirs(UPLOAD_PATH, exist_ok=True)
        
        for file in uploaded_files:
            if file.filename:
                # First secure the original filename
                original_filename = secure_filename(file.filename)
                
                # Get extension from the secured filename
                _, ext = os.path.splitext(original_filename)
                
                # Generate a unique filename with UUID
                unique_filename = f"{uuid.uuid4()}{ext}"
                
                # Create paths using os.path.join to ensure correct slashes for the OS
                file_path = os.path.join(UPLOAD_PATH, unique_filename)
                
                try:
                    # Save the file to the filesystem
                    file.save(file_path)
                    
                    # Create a web path with forward slashes for the database
                    web_path = f"/static/campsite_photos/{unique_filename}"
                    saved_file_paths.append(web_path)
                    
                    print(f"Successfully saved file to {file_path}")
                except Exception as e:
                    print(f"Error saving file: {e}")
    
    return saved_file_paths


@app_blueprint.route("/", methods=["GET", "POST"])
def index(curr_modal=None):
    # auth forms setup
    register_form: RegisterForm = session.pop("register_form", None) or RegisterForm()
    register_form_handler: FormHandler = FormHandler(register_form)

    login_form: LoginForm = session.pop("login_form", None) or LoginForm()
    login_form_handler: FormHandler = FormHandler(login_form)

    create_site_form: CreateSiteForm = session.pop("create_site_form", None) or CreateSiteForm(current_app)

    
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
        highest_rated_campsites_by_overall = [Campsite(current_app, **raw_site) for raw_site in highest_rated_campsites_by_overall_raw]
    if user_created_campsites_raw:
        user_created_campsites = [Campsite(current_app, **raw_site) for raw_site in user_created_campsites_raw]
    
    
    print(user_created_campsites or "campsites not bundled")
    

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
                login_user(User(user_ID=cursor.lastrowid))

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
    create_site_form = CreateSiteForm(current_app)
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
    else:
        return redirect(url_for("app_blueprint.index", curr_modal="create-site-modal"))
                    
                
@app_blueprint.route("/search-by-location", methods=["GET"])
def search_by_location():
    search_type = request.args.get("search-type")
    search_term = f"%{request.args.get("search-term")}%"
    site_ids = campsite_manager.fetch_by_areas(current_app, search_type, search_term, 0, 9)

    if (len(site_ids) < 1):
        return jsonify({
            "status": 200,
            "count": 0,
            "message": f"No site found under {search_type} {search_term}",
            "campsites": [],
            "success": True
        })

    sites = None
    with current_app.retrieve_db_connection() as (connection, cursor):
        try:
            cursor.execute(f"SELECT * FROM site WHERE site_ID IN {tuple(site_ids)}")
        except Exception as e:
            logging.error(f"failure to retrieve site by location type and name from site : {e}")
        else:
            sites = [Campsite(current_app, **row).serialize() for row in cursor.fetchall()]
    return jsonify({
            "status": 200,
            "count": len(sites),
            "message": "Sites found",
            "campsites": sites,
            "success": True
        })


@app_blueprint.route("/campsite", methods=["GET"])
def campsite():
    rating_site_form: RatingSiteForm = RatingSiteForm()
    rating_site_form_handler: FormHandler = FormHandler(rating_site_form)
    
    comment_site_form: CommentSiteForm = CommentSiteForm()
    comment_site_form_handler: FormHandler = FormHandler(comment_site_form)
    
    register_form: RegisterForm = session.pop("register_form", None) or RegisterForm()
    register_form_handler: FormHandler = FormHandler(register_form)

    login_form: LoginForm = session.pop("login_form", None) or LoginForm()
    login_form_handler: FormHandler = FormHandler(login_form)

    create_site_form: CreateSiteForm = session.pop("create_site_form", None) or CreateSiteForm(current_app)

    campsite_id = request.args.get("site_ID")
    if not campsite_id:
        return redirect(url_for("app_blueprint.index"))
    
    with current_app.retrieve_db_connection() as (connection, cursor):
        cursor.execute("SELECT * FROM site WHERE site_ID = %s", (campsite_id,))
        campsite = Campsite(current_app, **cursor.fetchone())
    return render_template("site.html", campsite=campsite,
                           register_form=register_form,
        register_form_handler=register_form_handler,
        login_form=login_form,
        login_form_handler=login_form_handler,
        create_site_form=create_site_form,
        comment_site_form=comment_site_form,
        comment_site_form_handler=comment_site_form_handler,
        rating_site_form_handler=rating_site_form_handler,
        rating_site_form=rating_site_form)

@app_blueprint.route("/campsite/rate", methods=["POST"])
@login_required
def rate_campsite():
    rating_site_form = RatingSiteForm()
    if rating_site_form.validate_on_submit():
        site_id = request.form.get("site_id")
        cleanliness_rating = rating_site_form.cleanliness_rating.data
        accessibility_rating = rating_site_form.accessibility_rating.data
        quietness_rating = rating_site_form.quietness_rating.data
        activities_rating = rating_site_form.activities_rating.data
        amenities_rating = rating_site_form.amenities_rating.data
        cost_rating = rating_site_form.cost_rating.data

        with current_app.retrieve_db_connection() as (connection, cursor):
            try:
                cursor.execute("""INSERT INTO rating (cleanliness, accessibility, quietness, activities, amenities, cost, site_ID)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                                (cleanliness_rating, accessibility_rating, quietness_rating,
                                 activities_rating, amenities_rating, cost_rating, site_id))
            except Exception as e:
                logging.error(f"failure to insert new site rating : {e}")
                connection.rollback()
            else:
                connection.commit()
    return redirect(url_for("app_blueprint.campsite", site_ID=site_id))


@app_blueprint.route("/campsite/comment", methods=["POST"])
@login_required
def comment_campsite():
    comment_site_form = CommentSiteForm()
    if comment_site_form.validate_on_submit():
        site_id = request.form.get("site_id")
        comment = comment_site_form.comment.data

        with current_app.retrieve_db_connection() as (connection, cursor):
            try:
                cursor.execute("""INSERT INTO comment (comment, timestamp, user_ID, site_ID)
                                VALUES (%s, CURRENT_DATE(), %s, %s)""",
                                (comment, current_user.id, site_id))
            except Exception as e:
                logging.error(f"failure to insert new site : {e}")
                connection.rollback()
            else:
                connection.commit()
    return redirect(url_for("app_blueprint.campsite", site_ID=site_id))

    
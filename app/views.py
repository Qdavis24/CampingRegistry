from flask import render_template, url_for, Blueprint

app_blueprint = Blueprint("app_blueprint", "app_blueprint")

@app_blueprint.route("/")
def index():
    return render_template( "index.html")
from .views import app_blueprint
import flask

def create_app():
    app = flask.Flask(__name__)
    app.config.from_pyfile("config.py")
    app.register_blueprint(app_blueprint)
    return app

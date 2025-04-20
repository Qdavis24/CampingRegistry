from .config import Config
from .views import app_blueprint
from flask import Flask, g
import mysql.connector

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        g.cursor = g.db.cursor(dictionary=True)
    return g.db, g.cursor

def close_db(e=None):
    db = g.pop('db', None)
    cursor = g.pop('cursor', None)
    
    if cursor is not None:
        cursor.close()
    
    if db is not None:
        db.close()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(app_blueprint)
    app.teardown_appcontext(close_db)
    return app

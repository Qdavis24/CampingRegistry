from .config import Config
from .views import app_blueprint
from .util_classes import User
from flask_login import LoginManager
from flask import Flask
from contextlib import contextmanager
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import MySQLConnection
import logging


logging.basicConfig(filename="./logs/last-run-log.txt", 
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.ERROR,
                    filemode="w")

# Set Werkzeug's logger level explicitly
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)

# Also set Flask's logger level
flask_logger = logging.getLogger('flask')
flask_logger.setLevel(logging.ERROR)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(app_blueprint)
    
    try:
        dbconfig = {
            "database": Config.MYSQL_DATABASE,
            "user": Config.MYSQL_USER,
            "host": Config.MYSQL_HOST,
            "password": Config.MYSQL_PASSWORD,
        }
        connection_pool = MySQLConnectionPool(
            pool_name="campsites_db_pool",
            pool_size=10,
            pool_reset_session=True,
            **dbconfig
        )
    except Exception as e:
        logging.error(e)
    else:
        app.db_pool = connection_pool

        @contextmanager
        def retrieve_db_connection():
            """
            yields connection and cursor then closes
            both when exiting with"""
            connection = None
            cursor = None
            try:
                connection: MySQLConnection = app.db_pool.get_connection()
                cursor: MySQLConnection.cursor = connection.cursor(dictionary=True)
                yield connection, cursor
            except Exception as e:
                logging.error(e)
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close() 
        app.retrieve_db_connection = retrieve_db_connection

        login_manager = LoginManager(app)

        @login_manager.user_loader
        def load_user(user_id):
            with retrieve_db_connection() as (connection, cursor):
                try:
                    cursor.execute("SELECT * FROM user WHERE user_ID = %s", (user_id,))
                    user_dict = cursor.fetchone()
                    user = User(**user_dict) if user_dict else None
                    print(user)
                except Exception as e:
                    print("here")
                    logging.error(f"failure to load user {e}")
            
            return user
            
        return app

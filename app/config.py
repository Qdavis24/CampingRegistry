from dotenv import load_dotenv
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG=True
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT  = os.getenv("MYSQL_PORT")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
    

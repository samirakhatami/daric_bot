import mysql.connector as mysql
import config

def conect_database():
    db = mysql.connect(
        host= config.host,
        user= config.username,
        passwd = config.pas,
        database = config.database
    )
    cr = db.cursor()
    return cr , db


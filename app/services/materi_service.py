from app.extensions.db import mysql

def get_all_materi():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM materi")
    return cursor.fetchall()

def get_materi_by_id(materi_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM materi WHERE id = %s", (materi_id,))
    return cursor.fetchone()

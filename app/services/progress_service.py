from app.extensions.db import mysql

def get_user_progress(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT * FROM user_progress
        WHERE user_id = %s
    """, (user_id,))
    return cursor.fetchall()

def update_user_progress(data):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE user_progress
        SET progress = %s
        WHERE user_id = %s AND provinsi_id = %s
    """, (data['progress'], data['user_id'], data['provinsi_id']))
    mysql.connection.commit()
    return {"message": "Progress berhasil diperbarui"}

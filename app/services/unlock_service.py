from app.extensions.db import mysql

def unlock_provinsi(data):
    user_id = data['user_id']
    pulau_id = data['pulau_id']
    provinsi_id = data['provinsi_id']

    cursor = mysql.connection.cursor()

    # Update atau insert user_progress menjadi unlocked
    cursor.execute("""
        SELECT id FROM user_progress
        WHERE user_id = %s AND provinsi_id = %s
    """, (user_id, provinsi_id))

    exists = cursor.fetchone()
    if exists:
        cursor.execute("""
            UPDATE user_progress
            SET unlocked = TRUE
            WHERE user_id = %s AND provinsi_id = %s
        """, (user_id, provinsi_id))
    else:
        cursor.execute("""
            INSERT INTO user_progress (user_id, pulau_id, provinsi_id, unlocked, lives, progress)
            VALUES (%s, %s, %s, TRUE, 5, 0)
        """, (user_id, pulau_id, provinsi_id))

    mysql.connection.commit()
    return {"message": "Provinsi berhasil dibuka"}
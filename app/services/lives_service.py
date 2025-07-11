from app.extensions.db import mysql

def get_lives(user_id, provinsi_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT lives FROM user_progress
        WHERE user_id = %s AND provinsi_id = %s
    """, (user_id, provinsi_id))
    result = cursor.fetchone()
    if result:
        return {"lives": result['lives']}
    return {"message": "Data tidak ditemukan"}, 404

def decrease_lives(data):
    user_id = data['user_id']
    provinsi_id = data['provinsi_id']
    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE user_progress SET lives = lives - 1
        WHERE user_id = %s AND provinsi_id = %s AND lives > 0
    """, (user_id, provinsi_id))
    mysql.connection.commit()
    return {"message": "Nyawa dikurangi"}

def reset_lives(data):
    user_id = data['user_id']
    provinsi_id = data['provinsi_id']
    jumlah = data['jumlah']
    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE user_progress SET lives = %s
        WHERE user_id = %s AND provinsi_id = %s
    """, (jumlah, user_id, provinsi_id))
    mysql.connection.commit()
    return {"message": f"Nyawa direset menjadi {jumlah}"}

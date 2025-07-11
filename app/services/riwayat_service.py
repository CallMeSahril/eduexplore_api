from app.extensions.db import mysql

def get_riwayat_by_user(user_id, provinsi_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT j.soal_id, j.jawaban, j.benar
        FROM jawaban_user j
        JOIN soal s ON j.soal_id = s.id
        WHERE j.user_id = %s AND s.provinsi_id = %s
        ORDER BY j.soal_id ASC
    """, (user_id, provinsi_id))
    return cursor.fetchall()
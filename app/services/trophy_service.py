from app.extensions.db import mysql

def get_user_trophy(user_id):
    cursor = mysql.connection.cursor()

    # Ambil trophy provinsi
    cursor.execute("""
        SELECT p.nama, t.ikon_url
        FROM trophy t
        JOIN provinsi p ON t.provinsi_id = p.id
        WHERE t.user_id = %s
    """, (user_id,))
    provinsi = cursor.fetchall()

    # Ambil trophy pulau
    cursor.execute("""
        SELECT pl.nama, t.ikon_url
        FROM trophy t
        JOIN pulau pl ON t.pulau_id = pl.id
        WHERE t.user_id = %s
    """, (user_id,))
    pulau = cursor.fetchall()

    return {
        "provinsi": provinsi,
        "pulau": pulau
    }

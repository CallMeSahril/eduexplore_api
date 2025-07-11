from app.extensions.db import mysql


def get_all_pulau_by_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT p.id, p.nama, p.ikon_url,
            CASE WHEN up.unlocked IS NULL THEN FALSE ELSE up.unlocked END AS unlocked
        FROM pulau p
        LEFT JOIN user_progress up ON up.pulau_id = p.id AND up.user_id = %s
        GROUP BY p.id
    """, (user_id,))
    return cursor.fetchall()


def get_provinsi_by_pulau(pulau_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT id, nama, ikon_url FROM provinsi WHERE pulau_id = %s
    """, (pulau_id,))
    return cursor.fetchall()


def get_map_by_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT 
            pl.id AS pulau_id, pl.nama AS pulau, pl.ikon_url AS pulau_ikon_url,
            pr.id AS provinsi_id, pr.nama AS nama, pr.ikon_url AS ikon_url,
            pr.x, pr.y,
            up.unlocked, up.selesai
        FROM provinsi pr
        JOIN pulau pl ON pr.pulau_id = pl.id
        LEFT JOIN user_progress up ON up.provinsi_id = pr.id AND up.user_id = %s
        ORDER BY pl.id, pr.id
    """, (user_id,))
    rows = cursor.fetchall()

    result = {}
    for row in rows:
        pulau = row['pulau']

        # Menentukan status berdasarkan unlocked dan selesai
        if row['unlocked'] is None or row['unlocked'] == 0:
            status = "terkunci"
        elif row['selesai']:
            status = "selesai"
        else:
            status = "terbuka"

        provinsi_data = {
            "nama": row['nama'],
            "provinsi_id": row['provinsi_id'],
            "ikon_url": row['ikon_url'],
            "x": row['x'],
            "y": row['y'],
            "pulau_id": row['pulau_id'],
            "pulau_ikon_url": row['pulau_ikon_url'],
            "unlocked": bool(row['unlocked']),
            "selesai": bool(row['selesai']),
            "status": status
        }

        if pulau not in result:
            result[pulau] = []
        result[pulau].append(provinsi_data)

    return result

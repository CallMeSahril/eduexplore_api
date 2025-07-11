from app.extensions.db import mysql
from flask import current_app
import MySQLdb


def register_user(data):
    required_fields = ['nama', 'email', 'password', 'kelas_id']

    # Cek field wajib
    for field in required_fields:
        if field not in data or not data[field]:
            return {"message": f"Field '{field}' wajib diisi."}, 400

    try:
        cursor = mysql.connection.cursor()

        # Cek apakah email sudah terdaftar
        check_query = "SELECT id FROM users WHERE email = %s"
        cursor.execute(check_query, (data['email'],))
        existing_user = cursor.fetchone()
        if existing_user:
            return {"message": "Email sudah terdaftar."}, 409

        # Lanjut proses registrasi
        insert_query = """
            INSERT INTO users (nama, email, password, kelas_id)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            data['nama'],
            data['email'],
            data['password'],  # sebaiknya di-hash sebelum disimpan!
            data['kelas_id']
        ))

        mysql.connection.commit()
        user_id = cursor.lastrowid

        return {"message": "Registrasi berhasil", "user_id": user_id}, 201

    except MySQLdb.Error as e:
        current_app.logger.error(f"MySQL Error: {str(e)}")
        return {"message": "Terjadi kesalahan saat registrasi."}, 500

    finally:
        cursor.close()


def login_user(data):
    try:
        cursor = mysql.connection.cursor()
        query = "SELECT id, nama, email, kelas_id FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (data['email'], data['password']))
        user = cursor.fetchone()
        if user:
            return {"token": "jwt_token", "user": user}, 200
        return {"message": "Email atau password salah"}, 401
    except Exception as e:
        print("Koneksi Error:", str(e))
        return {"message": "Internal server error"}, 500



def get_user_profile(user_id):
    cursor = mysql.connection.cursor()
    query = """
        SELECT u.id, u.nama, u.email, k.nama AS kelas, u.foto_profil
        FROM users u
        JOIN kelas k ON u.kelas_id = k.id
        WHERE u.id = %s
    """
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    if result:
        return result, 200
    return {"message": "User tidak ditemukan"}, 404


def register_user_with_progress(data):
    cursor = mysql.connection.cursor()

    # Simpan user baru
    cursor.execute("""
        INSERT INTO users (nama, email, password, kelas_id)
        VALUES (%s, %s, %s, %s)
    """, (data['nama'], data['email'], data['password'], data['kelas_id']))
    user_id = cursor.lastrowid

    # Inisialisasi progress untuk Pulau 1, Provinsi 1
    cursor.execute("""
        INSERT INTO user_progress (user_id, pulau_id, provinsi_id, progress, unlocked, lives,selesai)
        VALUES (%s, 1, 1, 0, TRUE, 5,0)
    """, (user_id,))

    mysql.connection.commit()
    return {"message": "Registrasi berhasil", "user_id": user_id}

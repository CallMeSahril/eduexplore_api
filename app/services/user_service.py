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


def delete_user(user_id):
    try:
        cursor = mysql.connection.cursor()

        # Cek apakah user ada
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            return {"message": "User tidak ditemukan"}, 404

        # Hapus dari tabel user_progress terlebih dahulu jika ada foreign key
        cursor.execute(
            "DELETE FROM user_progress WHERE user_id = %s", (user_id,))

        # Hapus user
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()

        return {"message": f"User dengan ID {user_id} berhasil dihapus"}, 200

    except MySQLdb.Error as e:
        current_app.logger.error(f"MySQL Error: {str(e)}")
        return {"message": "Terjadi kesalahan saat menghapus user"}, 500

    finally:
        cursor.close()


def change_user_password(user_id, data):
    try:
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not old_password or not new_password or not confirm_password:
            return {"message": "Semua field wajib diisi"}, 400

        if new_password != confirm_password:
            return {"message": "Konfirmasi password tidak cocok"}, 400

        cursor = mysql.connection.cursor()

        # Cek apakah user ada dan password lama cocok
        cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        if not result:
            return {"message": "User tidak ditemukan"}, 404

        current_password = result[0]
        if current_password != old_password:
            return {"message": "Password lama salah"}, 401

        # Update password
        cursor.execute(
            "UPDATE users SET password = %s WHERE id = %s", (new_password, user_id))
        mysql.connection.commit()

        return {"message": "Password berhasil diubah"}, 200

    except MySQLdb.Error as e:
        current_app.logger.error(f"MySQL Error: {str(e)}")
        return {"message": "Terjadi kesalahan saat mengubah password"}, 500

    finally:
        cursor.close()

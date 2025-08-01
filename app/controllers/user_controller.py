from app.extensions.db import mysql
from flask_restx import Namespace, Resource
from app.services.user_service import get_user_profile

api = Namespace('user', description='User operations')


@api.route('/profile/<int:user_id>')
class UserProfile(Resource):
    def get(self, user_id):
        return get_user_profile(user_id)


# ==== Contoh File: app/services/user_service.py ====


def register_user(data):
    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO users (nama, email, password, kelas_id)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (data['nama'], data['email'],
                   data['password'], data['kelas_id']))
    mysql.connection.commit()
    user_id = cursor.lastrowid
    return {"message": "Registrasi berhasil", "user_id": user_id}, 201


def login_user(data):
    cursor = mysql.connection.cursor()
    query = "SELECT id, nama, email, kelas_id FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (data['email'], data['password']))
    user = cursor.fetchone()
    if user:
        return {"token": "jwt_token", "user": user}, 200
    return {"message": "Email atau password salah"}, 401


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


def delete_user(user_id):
    print(f"[DEBUG] Memulai proses hapus user ID: {user_id}")
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        print(f"[DEBUG] Hasil query SELECT: {user}")
        if not user:
            print("[DEBUG] User tidak ditemukan.")
            return {"message": "User tidak ditemukan"}, 404

        print("[DEBUG] Menghapus data dari user_progress...")
        cursor.execute("DELETE FROM user_progress WHERE user_id = %s", (user_id,))
        print("[DEBUG] Menghapus data dari users...")
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()

        print(f"[DEBUG] User dengan ID {user_id} berhasil dihapus.")
        return {"message": f"User dengan ID {user_id} berhasil dihapus"}, 200
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat menghapus user: {str(e)}")
        return {"message": f"Terjadi kesalahan: {str(e)}"}, 500
    finally:
        cursor.close()


def change_user_password(user_id, data):
    print(f"[DEBUG] Memulai proses ganti password untuk user ID: {user_id}")
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    print(f"[DEBUG] Data diterima: old={old_password}, new={new_password}, confirm={confirm_password}")

    if not old_password or not new_password or not confirm_password:
        print("[DEBUG] Ada field yang kosong.")
        return {"message": "Semua field wajib diisi"}, 400

    if new_password != confirm_password:
        print("[DEBUG] Konfirmasi password tidak cocok.")
        return {"message": "Konfirmasi password tidak cocok"}, 400

    cursor = mysql.connection.cursor()
    try:
        print("[DEBUG] Mengecek password lama...")
        cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        print(f"[DEBUG] Password sekarang di database: {result}")
        if not result:
            print("[DEBUG] User tidak ditemukan.")
            return {"message": "User tidak ditemukan"}, 404

        current_password = result[0]
        if current_password != old_password:
            print("[DEBUG] Password lama salah.")
            return {"message": "Password lama salah"}, 401

        print("[DEBUG] Password valid, mengupdate ke password baru...")
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_password, user_id))
        mysql.connection.commit()

        print("[DEBUG] Password berhasil diubah.")
        return {"message": "Password berhasil diubah"}, 200
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat mengubah password: {str(e)}")
        return {"message": f"Terjadi kesalahan: {str(e)}"}, 500
    finally:
        cursor.close()

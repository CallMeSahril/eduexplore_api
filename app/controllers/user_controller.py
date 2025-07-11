from flask_restx import Namespace, Resource
from app.services.user_service import get_user_profile

api = Namespace('user', description='User operations')

@api.route('/profile/<int:user_id>')
class UserProfile(Resource):
    def get(self, user_id):
        return get_user_profile(user_id)


# ==== Contoh File: app/services/user_service.py ====
from app.extensions.db import mysql

def register_user(data):
    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO users (nama, email, password, kelas_id)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (data['nama'], data['email'], data['password'], data['kelas_id']))
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

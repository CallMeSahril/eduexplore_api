from flask_restx import Namespace, Resource, fields
from app.extensions.db import mysql

api = Namespace('kelas', description='Operasi data kelas')

kelas_model = api.model('Kelas', {
    'id': fields.Integer,
    'nama_kelas': fields.String
})


@api.route('')
class KelasList(Resource):
    @api.marshal_list_with(kelas_model)
    def get(self):
        """Ambil semua data kelas"""
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM kelas ORDER BY id")
        data = cursor.fetchall()
        return data, 200

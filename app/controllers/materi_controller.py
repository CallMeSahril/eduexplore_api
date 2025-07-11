from flask_restx import Namespace, Resource, fields
from app.extensions.db import mysql

api = Namespace('materi', description='Materi operations')

materi_model = api.model('Materi', {
    'id': fields.Integer,
    'judul': fields.String,
    'file_pdf': fields.String
})

@api.route('/')
class ListMateri(Resource):
    @api.marshal_list_with(materi_model)
    def get(self):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM materi")
        materi = cursor.fetchall()
        return materi
    
@api.route('/<int:id>')
class DetailMateri(Resource):
    @api.marshal_with(materi_model)
    def get(self, id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM materi WHERE id = %s", (id,))
        materi = cursor.fetchone()
        if not materi:
            api.abort(404, "Materi tidak ditemukan")
        return materi

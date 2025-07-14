from flask_restx import Namespace, Resource, fields
from flask import request
from app.extensions.db import mysql

api = Namespace('pdf', description='PDF materi per kelas')

pdf_model = api.model('PDFMateri', {
    'id': fields.Integer,
    'kelas_id': fields.Integer,
    'judul': fields.String,
    'url_pdf': fields.String
})

read_input = api.model('PDFReadInput', {
    'user_id': fields.Integer(required=True, description='ID pengguna yang membaca PDF'),
    'kelas_id': fields.Integer(required=True, description='ID kelas yang ingin dibuka PDF-nya')
})


@api.route('/<int:kelas_id>')
class PDFByKelas(Resource):
    @api.marshal_list_with(pdf_model)
    def get(self, kelas_id):
        """Ambil daftar PDF berdasarkan kelas"""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM pdf_materi WHERE kelas_id = %s", (kelas_id,))
        result = cursor.fetchall()
        cursor.close()
        return result, 200


@api.route('/read')
class PDFRead(Resource):
    @api.expect(read_input)
    def post(self):
        """Update lives berdasarkan progress terakhir (jika belum penuh)"""
        data = request.json
        user_id = data.get('user_id')
        kelas_id = data.get('kelas_id')

        if not user_id or not kelas_id:
            return {"message": "user_id dan kelas_id wajib diisi"}, 400

        cursor = mysql.connection.cursor()

        # Ambil progress terakhir milik user berdasarkan ID DESC
        cursor.execute("""
            SELECT id, provinsi_id, lives 
            FROM user_progress
            WHERE user_id = %s
            ORDER BY id DESC
            LIMIT 1
        """, (user_id,))
        last_progress = cursor.fetchone()

        provinsi_updated = 0

        if last_progress:
            if last_progress['lives'] < 5:
                cursor.execute("""
                    UPDATE user_progress
                    SET lives = lives + 1
                    WHERE id = %s
                """, (last_progress['id'],))
                provinsi_updated = 1
            else:
                cursor.close()
                return {
                    "message": "Lives sudah maksimal (5).",
                    "updated_lives": 0
                }, 200
        else:
            # Jika user belum punya progress sama sekali, unlock provinsi pertama
            cursor.execute("""
                SELECT id, pulau_id FROM provinsi ORDER BY id ASC LIMIT 1
            """)
            prov_row = cursor.fetchone()
            if prov_row:
                cursor.execute("""
                    INSERT INTO user_progress (user_id, provinsi_id, pulau_id, unlocked, lives)
                    VALUES (%s, %s, %s, TRUE, 5)
                """, (user_id, prov_row['id'], prov_row['pulau_id']))
                provinsi_updated = 1

        mysql.connection.commit()
        cursor.close()

        return {
            'message': 'Lives diperbarui.' if provinsi_updated else 'Tidak ada update.',
            'updated_lives': provinsi_updated
        }, 200

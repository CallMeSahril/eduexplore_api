from flask_restx import Namespace, Resource, fields
from app.services.riwayat_service import get_riwayat_by_user

api = Namespace('riwayat', description='Riwayat jawaban user')

riwayat_model = api.model('RiwayatJawaban', {
    'soal_id': fields.Integer,
    'jawaban': fields.String,
    'benar': fields.Boolean
})

@api.route('/<int:user_id>/provinsi/<int:provinsi_id>')
class RiwayatPerProvinsi(Resource):
    @api.marshal_list_with(riwayat_model)
    def get(self, user_id, provinsi_id):
        return get_riwayat_by_user(user_id, provinsi_id)


from flask_restx import Namespace, Resource, fields
from app.services.jawab_service import proses_jawaban

api = Namespace('jawab', description='Jawaban operations')

jawab_model = api.model('JawabRequest', {
    'user_id': fields.Integer(required=True),
    'soal_id': fields.Integer(required=True),
    'jawaban': fields.String(required=True, description='Jawaban user, misal A/B/C/D')
})

jawab_response = api.model('JawabResponse', {
    'benar': fields.Boolean,
    'message': fields.String,
    'feedback_ikon_url': fields.String,
    'sisa_lives': fields.Integer
})

@api.route('/')
class JawabSoal(Resource):
    @api.expect(jawab_model)
    @api.marshal_with(jawab_response)
    def post(self):
        data = api.payload
        return proses_jawaban(data)
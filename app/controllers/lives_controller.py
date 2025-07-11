from flask_restx import Namespace, Resource, fields
from app.services.lives_service import get_lives, decrease_lives, reset_lives

api = Namespace('lives', description='Lives (Nyawa) operations')

reset_model = api.model('ResetLives', {
    'user_id': fields.Integer(required=True),
    'provinsi_id': fields.Integer(required=True),
    'jumlah': fields.Integer(required=True)
})

kurangi_model = api.model('KurangiLives', {
    'user_id': fields.Integer(required=True),
    'provinsi_id': fields.Integer(required=True)
})

@api.route('/<int:user_id>/<int:provinsi_id>')
class AmbilLives(Resource):
    def get(self, user_id, provinsi_id):
        return get_lives(user_id, provinsi_id)

@api.route('/decrease')
class KurangiLives(Resource):
    @api.expect(kurangi_model)
    def post(self):
        return decrease_lives(api.payload)

@api.route('/reset')
class ResetLives(Resource):
    @api.expect(reset_model)
    def post(self):
        return reset_lives(api.payload)

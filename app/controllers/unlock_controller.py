from flask_restx import Namespace, Resource, fields
from app.services.unlock_service import unlock_provinsi

api = Namespace('unlock', description='Unlock provinsi/pulau')

unlock_model = api.model('UnlockModel', {
    'user_id': fields.Integer(required=True),
    'pulau_id': fields.Integer(required=True),
    'provinsi_id': fields.Integer(required=True)
})

@api.route('/')
class UnlockProvinsi(Resource):
    @api.expect(unlock_model)
    def post(self):
        return unlock_provinsi(api.payload)

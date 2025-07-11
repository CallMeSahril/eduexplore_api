from flask_restx import Namespace, Resource, fields
from app.services.progress_service import get_user_progress, update_user_progress

api = Namespace('progress', description='Progress operations')

progress_model = api.model('Progress', {
    'user_id': fields.Integer,
    'provinsi_id': fields.Integer,
    'pulau_id': fields.Integer,
    'progress': fields.Integer,
    'unlocked': fields.Boolean,
    'lives': fields.Integer
})

update_model = api.model('UpdateProgress', {
    'user_id': fields.Integer(required=True),
    'provinsi_id': fields.Integer(required=True),
    'progress': fields.Integer(required=True)
})

@api.route('/<int:user_id>')
class GetProgress(Resource):
    @api.marshal_list_with(progress_model)
    def get(self, user_id):
        return get_user_progress(user_id)

@api.route('/update')
class UpdateProgress(Resource):
    @api.expect(update_model)
    def post(self):
        data = api.payload
        return update_user_progress(data)


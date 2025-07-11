# ==== Contoh File: app/controllers/auth_controller.py ====
from flask_restx import Namespace, Resource, fields
from app.services.user_service import register_user_with_progress, login_user

api = Namespace('auth', description='Auth operations')

register_model = api.model('Register', {
    'nama': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'kelas_id': fields.Integer(required=True)
})

login_model = api.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})


@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        data = api.payload
        return register_user_with_progress(data)


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        data = api.payload
        return login_user(data)

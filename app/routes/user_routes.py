from flask_restx import Namespace, Resource
from app.services.user_service import get_user_profile, delete_user
from app.services.user_service import change_user_password

api = Namespace('user', description='User operations')


@api.route('/profile/<int:user_id>')
class UserProfile(Resource):
    def get(self, user_id):
        return get_user_profile(user_id)


@api.route('/<int:user_id>')
class UserDelete(Resource):
    def delete(self, user_id):
        return delete_user(user_id)


@api.route('/change-password/<int:user_id>')
class ChangePassword(Resource):
    def put(self, user_id):
        data = request.get_json()
        return change_user_password(user_id, data)

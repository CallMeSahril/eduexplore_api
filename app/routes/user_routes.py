from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.user_service import get_user_profile, delete_user
from app.services.user_service import change_user_password
from flask import request  # ← tambahkan ini

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile/<int:user_id>')
class UserProfile(Resource):
    def get(self, user_id):
        return get_user_profile(user_id)


@user_bp.route('/<int:user_id>')
class UserDelete(Resource):
    def delete(self, user_id):
        return delete_user(user_id)


@user_bp.route('/change-password/<int:user_id>')
class ChangePassword(Resource):
    def put(self, user_id):
        data = request.get_json()
        return change_user_password(user_id, data)

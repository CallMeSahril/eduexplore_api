from flask_restx import fields

def get_user_model(api):
    return api.model('User', {
        'id': fields.Integer(),
        'nama': fields.String(),
        'email': fields.String(),
        'kelas': fields.String(),
        'foto_profil': fields.String()
    })

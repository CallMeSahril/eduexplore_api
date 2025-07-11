from flask_restx import Namespace, Resource, fields
from app.services.pulau_service import get_all_pulau_by_user, get_provinsi_by_pulau, get_map_by_user

api = Namespace('pulau', description='Pulau dan Provinsi')

pulau_model = api.model('Pulau', {
    'id': fields.Integer,
    'nama': fields.String,
    'ikon_url': fields.String,
    'unlocked': fields.Boolean
})

provinsi_model = api.model('Provinsi', {
    'id': fields.Integer,
    'nama': fields.String,
    'ikon_url': fields.String
})


@api.route('/<int:user_id>')
class ListPulau(Resource):
    @api.marshal_list_with(pulau_model)
    def get(self, user_id):
        return get_all_pulau_by_user(user_id)


@api.route('/<int:pulau_id>/provinsi')
class ListProvinsi(Resource):
    @api.marshal_list_with(provinsi_model)
    def get(self, pulau_id):
        return get_provinsi_by_pulau(pulau_id)


@api.route('/map/<int:user_id>')
class MapProgress(Resource):
    def get(self, user_id):
        result = get_map_by_user(user_id)
        sorted_result = sorted(result.items(), key=lambda x: x[1][0]["pulau_id"] if x[1] else 0)
        return [
            {
                "pulau": group["pulau_id"],
                "pulau_nama": pulau,
                "pulau_ikon_url": group["pulau_ikon_url"],
                "provinsi": [
                    {
                        "nama": pr["nama"],
                        "provinsi": pr["provinsi_id"],
                        "ikon_url": pr["ikon_url"],
                        "x": pr["x"],
                        "y": pr["y"],
                        "status": pr.get("status", "terbuka")
                    }
                    for pr in provinsis
                ]
            }
            for pulau, provinsis in sorted_result if provinsis for group in [provinsis[0]]
        ]

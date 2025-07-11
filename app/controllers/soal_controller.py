from flask_restx import Namespace, Resource, reqparse
from app.services.soal_service import get_soal_by_provinsi
from app.models.soal_model import get_soal_model

api = Namespace('soal', description='Soal operations')
soal_model = get_soal_model(api)

# Parser untuk query param kelas_id dan page
parser = reqparse.RequestParser()
parser.add_argument('kelas_id', type=int, required=True, help='ID kelas diperlukan')
parser.add_argument('page', type=int, required=True, help='Halaman soal')
parser.add_argument('user_id', type=int, required=True, help='User ID')

@api.route('/<int:provinsi_id>')
class SoalByProvinsi(Resource):
    @api.expect(parser)
    @api.marshal_with(soal_model)
    def get(self, provinsi_id):
        args = parser.parse_args()
        kelas_id = args['kelas_id']
        page = args['page']
        user_id = args['user_id']
        return get_soal_by_provinsi(provinsi_id, kelas_id, user_id, page)

from flask import Blueprint
from flask_restx import Api
from app.controllers.auth_controller import api as auth_ns
from app.controllers.user_controller import api as user_ns
from app.controllers.soal_controller import api as soal_ns
from app.controllers.jawab_controller import api as jawab_ns
from app.controllers.materi_controller import api as materi_ns
from app.controllers.progress_controller import api as progress_ns
from app.controllers.trophy_controller import api as trophy_ns
from app.controllers.lives_controller import api as lives_ns
from app.controllers.unlock_controller import api as unlock_ns
from app.controllers.riwayat_controller import api as riwayat_ns
from app.controllers.pulau_controller import api as pulau_ns
from app.controllers.kelas_controller import api as kelas_ns
from app.controllers.pdf_materi_api import api as pdf_ns
api_blueprint = Blueprint('api', __name__)

# Enable Swagger UI at /api/docs
api = Api(api_blueprint,
          title='Edu API',
          version='1.0',
          description='Dokumentasi API EduExplore',
          doc='/docs')  # <== Swagger UI akan diakses di /api/docs

# Register namespaces
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(user_ns, path='/user')
api.add_namespace(soal_ns, path='/soal')
api.add_namespace(jawab_ns, path='/jawab')
api.add_namespace(materi_ns, path='/materi')
api.add_namespace(progress_ns, path='/progress')
api.add_namespace(trophy_ns, path='/trophy')
api.add_namespace(lives_ns, path='/lives')
api.add_namespace(unlock_ns, path='/unlock')
api.add_namespace(riwayat_ns, path='/riwayat')
api.add_namespace(pulau_ns, path='/pulau')
api.add_namespace(kelas_ns, path='/kelas')
api.add_namespace(pdf_ns, path='/pdf')

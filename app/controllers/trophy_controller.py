from app.extensions.db import mysql
from flask_restx import Namespace, Resource, fields
from app.services.trophy_service import get_user_trophy

api = Namespace('trophy', description='Trophy (Pencapaian) operations')

penghargaan_model = api.model('TrophyItem', {
    'nama': fields.String,
    'ikon_url': fields.String
})

response_model = api.model('TrophyResponse', {
    'pulau': fields.List(fields.Nested(penghargaan_model)),
    'provinsi': fields.List(fields.Nested(penghargaan_model))
})


@api.route('/<int:user_id>')
class TrophyByUser(Resource):
    @api.marshal_with(response_model)
    def get(self, user_id):
        return get_user_trophy(user_id)


# ==== File: app/services/trophy_service.py ====


def get_user_trophy(user_id):
    cursor = mysql.connection.cursor()

    print(
        f"[DEBUG] Memulai proses pengambilan trophy untuk user_id: {user_id}")

    # Ambil semua provinsi yang sudah ditrophy user
    cursor.execute("""
        SELECT p.id, p.nama, p.pulau_id, t.ikon_url
        FROM trophy t
        JOIN provinsi p ON t.provinsi_id = p.id
        WHERE t.user_id = %s
    """, (user_id,))
    provinsi_trophies = cursor.fetchall()
    print(
        f"[DEBUG] Jumlah trophy provinsi yang ditemukan: {len(provinsi_trophies)}")
    print(f"[DEBUG] Data provinsi trophy: {provinsi_trophies}")

    # Kelompokkan jumlah trophy provinsi per pulau
    provinsi_per_pulau = {}
    for p in provinsi_trophies:
        pulau_id = p['pulau_id']
        if pulau_id not in provinsi_per_pulau:
            provinsi_per_pulau[pulau_id] = []
        provinsi_per_pulau[pulau_id].append(p)

    print(f"[DEBUG] Grup provinsi per pulau: {provinsi_per_pulau}")

    # Ambil semua data jumlah provinsi per pulau dari DB
    cursor.execute(
        "SELECT pulau_id, COUNT(*) as total FROM provinsi GROUP BY pulau_id")
    provinsi_count = {row['pulau_id']: row['total']
                      for row in cursor.fetchall()}
    print(f"[DEBUG] Jumlah total provinsi per pulau: {provinsi_count}")

    # Filter trophy pulau yang benar-benar lengkap semua provinsinya
    pulau_trophies = []
    for pulau_id, prov_list in provinsi_per_pulau.items():
        jumlah_trophy_user = len(prov_list)
        jumlah_total_provinsi = provinsi_count.get(pulau_id, 0)
        print(
            f"[DEBUG] Memeriksa pulau_id={pulau_id}: user={jumlah_trophy_user}, total={jumlah_total_provinsi}")

        if jumlah_trophy_user == jumlah_total_provinsi:
            # User telah menyelesaikan semua provinsi di pulau ini
            cursor.execute("""
                SELECT pl.nama, t.ikon_url
                FROM trophy t
                JOIN pulau pl ON t.pulau_id = pl.id
                WHERE t.user_id = %s AND t.pulau_id = %s
            """, (user_id, pulau_id))
            result = cursor.fetchone()
            print(f"[DEBUG] Trophy pulau ditemukan: {result}")
            if result:
                pulau_trophies.append(result)

    # Format provinsi trophies
    provinsi = [{'nama': p['nama'], 'ikon_url': p['ikon_url']}
                for p in provinsi_trophies]
    print(f"[DEBUG] Final trophy provinsi: {provinsi}")
    print(f"[DEBUG] Final trophy pulau: {pulau_trophies}")

    return {
        "provinsi": provinsi,
        "pulau": pulau_trophies
    }

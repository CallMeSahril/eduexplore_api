
from app.extensions.db import mysql
def get_soal_by_provinsi(provinsi_id, kelas_id, user_id, page):
    cursor = mysql.connection.cursor()

    # Ambil total soal untuk provinsi dan kelas tersebut
    cursor.execute("""
        SELECT COUNT(*) as total FROM soal
        WHERE provinsi_id = %s AND kelas_id = %s
    """, (provinsi_id, kelas_id))
    total_soal = cursor.fetchone()['total']

    # Ambil lives dari user_progress
    cursor.execute("""
        SELECT lives FROM user_progress
        WHERE user_id = %s AND provinsi_id = %s
    """, (user_id, provinsi_id))
    progress = cursor.fetchone()
    lives = progress['lives'] if progress else 0

    # Cek apakah nyawa habis
    if lives <= 0:
        return {
            "message": "Nyawa tidak cukup. Silakan reset atau tunggu untuk lanjut.",
            "lives": lives
        }, 403  # 403 Forbidden

    # Hitung offset dan ambil soal sesuai halaman
    limit = 1
    offset = (page - 1) * limit
    cursor.execute("""
        SELECT * FROM soal
        WHERE provinsi_id = %s AND kelas_id = %s
        ORDER BY id
        LIMIT %s OFFSET %s
    """, (provinsi_id, kelas_id, limit, offset))
    soal = cursor.fetchone()

    if not soal:
        return {"message": "Soal tidak ditemukan"}, 404

    # Bentuk respons soal lengkap
    response = {
        "id": soal['id'],
        "pertanyaan": soal['pertanyaan'],
        "gambar_soal": soal['gambar_url'],
        "lives": lives,
        "soal_ke": page,
        "total_soal": total_soal,
        "pilihan": {
            "A": {"teks": soal['pilihan_a']},
            "B": {"teks": soal['pilihan_b'] },
            "C": {"teks": soal['pilihan_c']},
            "D": {"teks": soal['pilihan_d']},
        }
    }

    return response, 200

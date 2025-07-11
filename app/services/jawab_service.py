from flask_mysqldb import MySQL
from app.extensions.db import mysql
from datetime import datetime
import traceback

# def proses_jawaban(data):
#     user_id = data['user_id']
#     soal_id = data['soal_id']
#     jawaban = data['jawaban']

#     cursor = mysql.connection.cursor()

#     # Ambil data soal dan jawaban benar
#     cursor.execute("SELECT * FROM soal WHERE id = %s", (soal_id,))
#     soal = cursor.fetchone()
#     if not soal:
#         return {"message": "Soal tidak ditemukan"}, 404

#     benar = jawaban.upper() == soal['jawaban_benar'].upper()

#     # Simpan jawaban user
#     cursor.execute("""
#         INSERT INTO jawaban_user (user_id, soal_id, jawaban, benar)
#         VALUES (%s, %s, %s, %s)
#     """, (user_id, soal_id, jawaban.upper(), benar))

#     # Kurangi nyawa jika salah
#     if not benar:
#         cursor.execute("""
#             UPDATE user_progress SET lives = lives - 1
#             WHERE user_id = %s AND provinsi_id = %s AND lives > 0
#         """, (user_id, soal['provinsi_id']))

#     # Ambil lives terbaru
#     cursor.execute("""
#         SELECT lives FROM user_progress
#         WHERE user_id = %s AND provinsi_id = %s
#     """, (user_id, soal['provinsi_id']))
#     lives = cursor.fetchone()['lives']

#     mysql.connection.commit()

#     return {
#         "benar": benar,
#         "message": "Jawaban kamu benar!" if benar else "Jawaban kamu salah.",
#         "feedback_ikon_url": f"https://cdn.app.com/notif/{'benar' if benar else 'salah'}.png",
#         "sisa_lives": lives
#     }, 200


def proses_jawaban(data):
    user_id = data['user_id']
    soal_id = data['soal_id']
    jawaban = data['jawaban']

    cursor = mysql.connection.cursor()

    # Ambil data soal
    cursor.execute("SELECT * FROM soal WHERE id = %s", (soal_id,))
    soal = cursor.fetchone()
    if not soal:
        return {"message": "Soal tidak ditemukan"}, 404

    provinsi_id = soal['provinsi_id']
    benar = jawaban.upper() == soal['jawaban_benar'].upper()
    feedback_url = f"https://cdn.app.com/notif/{'benar' if benar else 'salah'}.png"

    # Simpan jawaban user ke jawaban_user
    cursor.execute("""
        INSERT INTO jawaban_user (user_id, soal_id, jawaban, benar, feedback_ikon_url)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, soal_id, jawaban.upper(), benar, feedback_url))

    # Kurangi nyawa jika salah
    if not benar:
        cursor.execute("""
            UPDATE user_progress SET lives = lives - 1
            WHERE user_id = %s AND provinsi_id = %s AND lives > 0
        """, (user_id, provinsi_id))

    # Ambil nyawa terbaru
    cursor.execute("""
        SELECT lives FROM user_progress
        WHERE user_id = %s AND provinsi_id = %s
    """, (user_id, provinsi_id))
    lives = cursor.fetchone()['lives']

    # Hitung soal_ke dan total_soal
    cursor.execute("""
        SELECT COUNT(*) AS total_dijawab
        FROM jawaban_user ju
        JOIN soal s ON ju.soal_id = s.id
        WHERE ju.user_id = %s AND s.provinsi_id = %s
    """, (user_id, provinsi_id))
    soal_ke = cursor.fetchone()['total_dijawab']

    cursor.execute(
        "SELECT COUNT(*) AS total_soal FROM soal WHERE provinsi_id = %s", (provinsi_id,))
    total_soal = cursor.fetchone()['total_soal']

    cek_dan_naik_level(user_id, provinsi_id, lives)

    mysql.connection.commit()

    return {
        "benar": benar,
        "message": "Jawaban kamu benar!" if benar else "Jawaban kamu salah.",
        "feedback_ikon_url": feedback_url,
        "sisa_lives": lives
    }, 200


def cek_dan_naik_level(user_id, provinsi_id, lives):
    try:
        cursor = mysql.connection.cursor()

        print("🟡 Cek provinsi dan ambil pulau_id...")
        cursor.execute(
            "SELECT pulau_id FROM provinsi WHERE id = %s", (provinsi_id,))
        pulau_result = cursor.fetchone()
        if not pulau_result:
            print(f"❌ Provinsi ID {provinsi_id} tidak ditemukan.")
            return
        pulau_id = pulau_result['pulau_id']
        print(f"✅ Dapat pulau_id: {pulau_id}")

        print("🟡 Hitung jumlah jawaban benar...")
        cursor.execute("""
            SELECT COUNT(*) AS benar
            FROM jawaban_user ju
            JOIN soal s ON ju.soal_id = s.id
            WHERE ju.user_id = %s AND s.provinsi_id = %s AND ju.benar = TRUE
        """, (user_id, provinsi_id))
        jumlah_benar = cursor.fetchone()['benar']
        print(f"📌 Jumlah benar di provinsi {provinsi_id}: {jumlah_benar}")

        if jumlah_benar >= 1:
            print("✅ Jumlah cukup. Update selesai & insert trophy provinsi...")
            cursor.execute("""
                UPDATE user_progress
                SET selesai = TRUE
                WHERE user_id = %s AND provinsi_id = %s
            """, (user_id, provinsi_id))

            print("🟢 Coba insert trophy provinsi...")
            cursor.execute(
                "SELECT pulau_id, ikon_url FROM provinsi WHERE id = %s", (provinsi_id,))

            provinsi_data = cursor.fetchone()
            ikon_url = provinsi_data['ikon_url']
            cursor.execute("""
                INSERT INTO trophy (user_id, provinsi_id, pulau_id, trophy_name, date_awarded, ikon_url)
                SELECT %s, %s, %s, %s, %s, %s
                FROM DUAL
                WHERE NOT EXISTS (
                    SELECT 1 FROM trophy WHERE user_id = %s AND provinsi_id = %s
                )
            """, (
                user_id, provinsi_id, pulau_id, f"Trophy Provinsi {provinsi_id}",
                datetime.now(), ikon_url,
                user_id, provinsi_id
            ))

            print("🟡 Hitung total dan selesai provinsi...")
            cursor.execute(
                "SELECT COUNT(*) AS total FROM provinsi WHERE pulau_id = %s", (pulau_id,))
            total_prov = cursor.fetchone()['total']

            cursor.execute("""
                SELECT COUNT(*) AS selesai
                FROM user_progress up
                JOIN provinsi p ON up.provinsi_id = p.id
                WHERE up.user_id = %s AND up.selesai = TRUE AND p.pulau_id = %s
            """, (user_id, pulau_id))
            selesai_prov = cursor.fetchone()['selesai']
            print(
                f"🌍 Total di pulau {pulau_id}: {total_prov}, Selesai: {selesai_prov}")

            if selesai_prov == total_prov:
                print("🏆 Semua provinsi selesai, insert trophy pulau...")
                cursor.execute("""
                    INSERT INTO trophy (user_id, provinsi_id, pulau_id, trophy_name, date_awarded, ikon_url)
                    SELECT %s, NULL, %s, %s, %s, %s
                    FROM DUAL
                    WHERE NOT EXISTS (
                        SELECT 1 FROM trophy WHERE user_id = %s AND pulau_id = %s
                    )
                """, (
                    user_id, pulau_id, f"Trophy Pulau {pulau_id}", datetime.now(
                    ),
                    "trophy-pulau.png", user_id, pulau_id
                ))

            print("🔓 Coba cari provinsi berikutnya...")
            cursor.execute("""
                SELECT pr.id, pr.pulau_id FROM provinsi pr
                JOIN pulau pl ON pr.pulau_id = pl.id
                WHERE (pr.id > %s OR pl.id > (SELECT pulau_id FROM provinsi WHERE id = %s))
                ORDER BY pl.id, pr.id
                LIMIT 1
            """, (provinsi_id, provinsi_id))
            next_prov = cursor.fetchone()

            if next_prov:
                next_id = next_prov['id']
                next_pulau_id = next_prov['pulau_id']
                print(f"🔓 Buka provinsi selanjutnya: {next_id}")
                cursor.execute("""
        INSERT INTO user_progress (user_id, pulau_id, provinsi_id, unlocked, selesai, lives)
        VALUES (%s, %s, %s, TRUE, FALSE, %s)
        ON DUPLICATE KEY UPDATE unlocked = TRUE
    """, (user_id, next_pulau_id, next_id, lives)),
            else:
                print("✅ Semua provinsi selesai, tidak ada level lanjut.")
        else:
            print("❌ Jumlah benar belum cukup.")

        mysql.connection.commit()
        cursor.close()

    except Exception as e:
        print("🚨 ERROR TERJADI SAAT cek_dan_naik_level 🚨")
        print(traceback.format_exc())


def simpan_jawaban(user_id, soal_id, jawaban, is_benar, provinsi_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO riwayat_jawaban (user_id, soal_id, jawaban, is_benar, provinsi_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, soal_id, jawaban, is_benar, provinsi_id))

    # Cek total jawaban user untuk provinsi ini
    cursor.execute("""
        SELECT COUNT(*) AS total FROM riwayat_jawaban
        WHERE user_id = %s AND provinsi_id = %s
    """, (user_id, provinsi_id))
    total = cursor.fetchone()['total']

    if total == 10:
        from app.services.pulau_service import cek_dan_naik_level
        cek_dan_naik_level(user_id, provinsi_id)

    mysql.connection.commit()

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions.db import mysql

soal_bp = Blueprint('soal', __name__)

# Tampilkan 10 soal
@soal_bp.route('/soal')
def tampil_soal():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM soal")
    soal = cursor.fetchall()
    return render_template('soal_list.html', soal=soal)

# Tambah soal (GET form dan POST simpan)
@soal_bp.route('/soal/tambah', methods=['GET', 'POST'])
def tambah_soal():
    if request.method == 'POST':
        data = request.form
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO soal (pertanyaan, keterangan, gambar_url, pilihan_a, pilihan_b, pilihan_c, pilihan_d,
                              jawaban_benar, provinsi_id, kelas_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            data['pertanyaan'], data['keterangan'], data['gambar_url'],
            data['pilihan_a'], data['pilihan_b'], data['pilihan_c'], data['pilihan_d'],
            data['jawaban_benar'], data['provinsi_id'], data['kelas_id']
        ))
        mysql.connection.commit()
        flash('Soal berhasil ditambahkan', 'success')
        return redirect(url_for('soal.tampil_soal'))
    return render_template('soal_form.html', soal=None)

# Edit soal (GET form dan POST update)
@soal_bp.route('/soal/edit/<int:id>', methods=['GET', 'POST'])
def edit_soal(id):
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        data = request.form
        cursor.execute("""
            UPDATE soal SET pertanyaan=%s, keterangan=%s, gambar_url=%s,
            pilihan_a=%s, pilihan_b=%s, pilihan_c=%s, pilihan_d=%s,
            jawaban_benar=%s, provinsi_id=%s, kelas_id=%s
            WHERE id=%s
        """, (
            data['pertanyaan'], data['keterangan'], data['gambar_url'],
            data['pilihan_a'], data['pilihan_b'], data['pilihan_c'], data['pilihan_d'],
            data['jawaban_benar'], data['provinsi_id'], data['kelas_id'], id
        ))
        mysql.connection.commit()
        flash('Soal berhasil diperbarui', 'success')
        return redirect(url_for('soal.tampil_soal'))

    cursor.execute("SELECT * FROM soal WHERE id = %s", (id,))
    soal = cursor.fetchone()
    return render_template('soal_form.html', soal=soal)

# Hapus soal
@soal_bp.route('/soal/hapus/<int:id>')
def hapus_soal(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM soal WHERE id = %s", (id,))
    mysql.connection.commit()
    flash('Soal berhasil dihapus', 'danger')
    return redirect(url_for('soal.tampil_soal'))

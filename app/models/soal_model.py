from flask_restx import fields

def get_soal_model(api):
    return api.model('Soal', {
        'id': fields.Integer,
        'pertanyaan': fields.String,
        'gambar_soal': fields.String,
        'lives': fields.Integer,
        'soal_ke': fields.Integer,
        'total_soal': fields.Integer,
        'pilihan': fields.Nested(api.model('PilihanJawaban', {
            'A': fields.Nested(api.model('JawabanA', {
                'teks': fields.String,
            })),
            'B': fields.Nested(api.model('JawabanB', {
                'teks': fields.String,
            })),
            'C': fields.Nested(api.model('JawabanC', {
                'teks': fields.String,
            })),
            'D': fields.Nested(api.model('JawabanD', {
                'teks': fields.String,
            }))
        }))
    })

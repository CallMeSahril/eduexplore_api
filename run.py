# ==== Contoh File: run.py ====
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port="5020", host="0.0.0.0", debug=True)

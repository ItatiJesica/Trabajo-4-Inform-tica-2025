from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_frecuente = db.Column(db.String(100))
    valoracion = db.Column(db.Integer)
    tipo_contenido = db.Column(db.String(50))
    frecuencia = db.Column(db.String(50))
    identificacion_contenido = db.Column(db.Integer)
    percepcion_identidad = db.Column(db.String(20))
    emociones = db.Column(db.String(200))
    cambio_comportamiento = db.Column(db.String(10))
    deseo_variedad = db.Column(db.String(20))

@app.route('/', methods=['GET', 'POST'])
def encuesta():
    if request.method == 'POST':
        nueva_respuesta = Respuesta(
            app_frecuente=request.form['app_frecuente'],
            valoracion=int(request.form['valoracion']),
            tipo_contenido=request.form['tipo_contenido'],
            frecuencia=request.form['frecuencia'],
            identificacion_contenido=int(request.form['identificacion_contenido']),
            percepcion_identidad=request.form['percepcion_identidad'],
            emociones=", ".join(request.form.getlist('emociones')),
            cambio_comportamiento=request.form['cambio_comportamiento'],
            deseo_variedad=request.form['deseo_variedad']
        )
        db.session.add(nueva_respuesta)
        db.session.commit()
        recomendacion = recomendar_app(nueva_respuesta.tipo_contenido, nueva_respuesta.frecuencia)
        return render_template('gracias.html',
                               app=nueva_respuesta.app_frecuente,
                               recomendacion=recomendacion,
                               identidad=nueva_respuesta.percepcion_identidad)
    return render_template('encuesta.html')

def recomendar_app(tipo_contenido, frecuencia):
    if tipo_contenido == 'Videos':
        if frecuencia in ['Varias veces al día', 'Una vez al día']:
            return 'TikTok o YouTube'
        else:
            return 'YouTube'
    elif tipo_contenido == 'Imágenes':
        return 'Instagram o Pinterest'
    elif tipo_contenido == 'Texto':
        return 'Twitter (ahora X) o Reddit'
    elif tipo_contenido == 'Combinado':
        return 'Facebook o Instagram'
    else:
        return 'Explorá nuevas apps como BeReal o Threads'

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('encuesta.db'):
            db.create_all()
    app.run(debug=True)

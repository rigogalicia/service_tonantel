from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from evaluacion import evaluacion, interrogante

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(evaluacion.Evaluacion, '/ed/<string:usr_conect>/<string:clave_conect>/<string:id_evaluacion>')
api.add_resource(interrogante.Interrogante, '/ed')

if __name__ == '__main__':
    app.run(debug=True)



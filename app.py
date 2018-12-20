from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from evaluacion import evaluacion, interrogante

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(evaluacion.Evaluacion, '/ed/evaluacion')
api.add_resource(interrogante.Interrogante, '/ed/interrogante')

if __name__ == '__main__':
    app.run(debug=True)
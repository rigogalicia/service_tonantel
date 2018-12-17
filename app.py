from flask import Flask
from flask_restful import Api
from evaluacion import evaluacion

app = Flask(__name__)
api = Api(app)

api.add_resource(evaluacion.Evaluacion, '/ed/<string:usr_conect>/<string:clave_conect>/<string:id_evaluacion>')

if __name__ == '__main__':
    app.run(debug=True)



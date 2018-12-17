from flask import Flask
from flask_restful import Api
from evaluacion import evaluacion

app = Flask(__name__)
api = Api(app)

api.add_resource(evaluacion.Evaluacion, '/ed')

if __name__ == '__main__':
    app.run(debug=True)



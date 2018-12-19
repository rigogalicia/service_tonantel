from flask_restful import Resource, reqparse
from db.mongo import Conexion

parser = reqparse.RequestParser()
parser.add_argument('id_evaluacion')
parser.add_argument('id_usuario')

class Interrogante(Resource):

    def __init__(self):
        ''' Metodo constructor de la clase '''
        self.__db = Conexion().get_db()


    def post(self):
        args = parser.parse_args()
        return args

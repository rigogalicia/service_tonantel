from flask_restful import Resource, reqparse
from db.mongo import Conexion
from bson.objectid import ObjectId

parser = reqparse.RequestParser()
parser.add_argument('id_evaluacion')
parser.add_argument('id_colaborador_conectado')
parser.add_argument('id_colaborador_calificar')
parser.add_argument('nombre_colaborador_calificar')
parser.add_argument('tipo_conducta')
parser.add_argument('id_interrogante')
parser.add_argument('interrogante')
parser.add_argument('ponderacion')
parser.add_argument('peso', type=int)

class Interrogante(Resource):

    def __init__(self):
        ''' Metodo constructor de la clase '''
        self.__db = Conexion().get_db()
        self.__args = parser.parse_args()

    def es_lider(self):
        ''' Este metodo determina si el usuario a calificar es lider o no '''

        collection = self.__db.colaboradores

        condicion = {
            '_id': self.__args['id_colaborador_calificar']
        }

        campos = {
            'subordinados': 1
        }

        resultado = collection.find_one(condicion, campos)

        if(len(resultado['subordinados']) > 0):
            return "SI"
        else:
            return "NO"
    
    def puesto_colaborador_calificar(self):
        ''' Este metodo devuelve el puesto del colaborador que se esta calificando '''
        collection = self.__db.colaboradores

        condicion = {
            '_id': self.__args['id_colaborador_calificar']
        }

        campos = {
            'puesto': 1
        }

        resultado = collection.find_one(condicion, campos)

        return resultado['puesto']

    def calcular_puntos(self):
        ''' Este metodo calcula la cantidad de puntos que le corresponden 
        a la interrogante de acuerdo a los criterios del usuario '''

        collection = self.__db.ed_interrogantes
        
        condicion = {
            'evaluacion': self.__args['id_evaluacion'],
            'conducta': self.__args['tipo_conducta'],
            'puesto': {'$in': [' ', self.puesto_colaborador_calificar()]},
            'lider': {'$in': ['NO', self.es_lider()]}
        }
        
        resultado = collection.find(condicion).count()

        puntos = (100 / resultado) * (self.__args['peso'] / 100) 
        
        return puntos
    
    def calificar_interrogante(self):
        ''' Este metodo se utiliza para calificar una interrogante '''
        
        collection = self.__db.ed_calificacion
        
        try:
            condicion = {
                '_id': self.__args['id_colaborador_conectado'] + self.__args['id_evaluacion']
            }
            
            informacion = {
                'id_interrogante': self.__args['id_interrogante'],
                'aspecto': self.__args['tipo_conducta'],
                'id_colaborador': self.__args['id_colaborador_calificar'],
                'nombre_colaborador': self.__args['nombre_colaborador_calificar'],
                'interrogante': self.__args['interrogante'],
                'ponderacion': self.__args['ponderacion'],
                'peso': self.__args['peso'],
                'puntos': self.calcular_puntos()
            }

            datos = {
                '$addToSet': {'cualitativo': informacion}
            }

            collection.update(condicion, datos)
            return '! La calificacion se realizo satisfactoriamente'
        except:
            return 'Error al calificar interrogante'

    def ponderaciones(self):
        ''' Este metodo consulta las ponderaciones de la evaluacion '''
        collection = self.__db.ed_evaluacion

        condicion = {
            '_id': ObjectId(self.__args['id_evaluacion'])
        }

        campos = {
            '_id': 0,
            'ponderaciones': 1
        }

        return collection.find_one(condicion, campos)

    def ids_interrogantes_calificadas(self):
        ''' Metodo para obtener una lista de los id 
        de las interrogantes ya calificadas '''
        
        collection = self.__db.ed_calificacion

        try:
            condicion = {
                "_id": self.__args['id_colaborador_conectado'] + self.__args['id_evaluacion']
            }

            campos = {
                '_id': 0,
                'cualitativo': 1
            }

            resultado = []
            data = collection.find_one(condicion, campos)
            for i in data['cualitativo']:
                resultado.append(ObjectId(i['id_interrogante']))
        except:
            resultado = []

        return resultado

    def progreso(self):
        ''' Este metodo calcula el progreso de calificacion '''
        collection = self.__db.ed_interrogantes

        condicion = {
            'evaluacion': self.__args['id_evaluacion'],
            'puesto': {'$in': [' ', self.puesto_colaborador_calificar()]},
            'lider': {'$in': ['NO', self.es_lider()]}
        }

        cantidad = collection.find(condicion).count()

        progreso = (100 * len(self.ids_interrogantes_calificadas())) / cantidad

        return progreso

    def datos_interrogante(self):
        ''' Este metodo califica una interrogante y obtiene los 
        datos de la siguiente interrogante '''

        if self.__args['id_interrogante'] != None:
            self.calificar_interrogante()
        
        collection = self.__db.ed_interrogantes

        condicion = {
            '_id': {'$nin': self.ids_interrogantes_calificadas()},
            'evaluacion': self.__args['id_evaluacion'],
            'lider': {'$in': ['NO', self.es_lider()]},
            'puesto': {'$in': [' ', self.puesto_colaborador_calificar()]}
        }

        res = collection.find_one(condicion)

        resultado = {
            'id_interrogante': str(res['_id']),
            'conducta': res['conducta'],
            'descripcion': res['descripcion']
        }

        resultado.update({'progreso': 'width: ' + str(self.progreso()) + '%'})
        resultado.update(self.ponderaciones())
        
        return resultado

    def post(self):
        ''' Metodo POST para iniciar la ejecucion de la clase '''
        self.__args = parser.parse_args()
        return self.datos_interrogante()

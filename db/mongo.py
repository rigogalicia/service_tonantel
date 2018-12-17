from pymongo import MongoClient

class Conexion():
    def __init__(self):
        __client = None
        __db = None

    def get_client(self):
        try:
            self.__client = MongoClient('localhost', 27017)
        except:
            print('! Error al conectarse a la base de datos MongoDB')
        
        return self.__client
    
    def get_db(self):
        try:
            self.__db = self.get_client().autorizacion
        except:
            print('! Error al conectarse a la base de datos MongoDB')
        
        return self.__db

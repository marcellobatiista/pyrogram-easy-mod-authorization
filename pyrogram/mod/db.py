import os
from pymongo import MongoClient


class DataBase:
    def __init__(self, host=None):
        if not host:
            self.host = os.environ['HOST_MONGODB']
        else:
            self.host = host

        self.mongodb = MongoClient(self.host)
        self.db = self.mongodb['Credenciais']

    def busca(self, _id, key=None):
        document = self.db.users.find_one({'_id': _id})
        if key:
            return document[key]
        return document
    
    def busca_by_referer(self, _id, key):
        return self.db.users.find_one({'referer': _id})[key]

    def atualiza(self, _id, key=None, value=None):
        if type(key) == dict and not value:
            self.db.users.update_one({'_id': _id}, {'$set': key})
        else:
            self.db.users.update_one({'_id': _id}, {'$set': {key: value}})
            
    def atualiza_by_referer(self, _id, key=None, value=None):
        if type(key) == dict and not value:
            self.db.users.update_one({'referer': _id}, {'$set': key})
        else:
            self.db.users.update_one({'referer': _id}, {'$set': {key: value}})

    def insere(self, dict):
        self.db.users.insert_one(dict)

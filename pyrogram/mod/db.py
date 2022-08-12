import os
from motor.motor_asyncio import AsyncIOMotorClient

class DataBase:
    def __init__(self, host=None):
        if not host:
            self.host = os.environ['HOST_MONGODB']
        else:
            self.host = host

        self.mongodb = AsyncIOMotorClient(self.host)
        self.db = self.mongodb['Credenciais']

    async def busca(self, _id, key=None):
        document = await self.db.users.find_one({'_id': _id})
        if key:
            return document[key]
        return document

    async def busca_by_referer(self, _id, key):
        result = await self.db.users.find_one({'referer': _id})
        return result[key]

    async def atualiza(self, _id, key=None, value=None):
        if type(key) == dict and not value:
            await self.db.users.update_one({'_id': _id}, {'$set': key})
        else:
            await self.db.users.update_one({'_id': _id}, {'$set': {key: value}})

    async def atualiza_by_referer(self, _id, key=None, value=None):
        if type(key) == dict and not value:
            await self.db.users.update_one({'referer': _id}, {'$set': key})
        else:
            await self.db.users.update_one({'referer': _id}, {'$set': {key: value}})

    async def insere(self, dict):
        await self.db.users.insert_one(dict)

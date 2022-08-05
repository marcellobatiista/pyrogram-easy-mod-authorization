from pyrogram import Client as Origem

# <> #
from pyrogram.mod.auth_web import AuthWeb
from pyrogram.mod.db import DataBase


class Client:
    def __init__(self,
                 phone,
                 pymongo_host=None,
                 input=False,
                 referer=None):

        self.db = DataBase(pymongo_host)
        self.input = input
        self.phone = phone
        self.referer = referer
        self.user = AuthWeb(self.db, self.input, self.referer).authorization(phone)

    def login(self, session):
        return Origem(session,
                      in_memory=True,
                      api_id=self.user['api_id'],
                      api_hash=self.user['api_hash'],
                      phone_number=self.phone,
                      dbmod=self.db,
                      inputmod=self.input)

    async def get_session(self):
        if self.user['session_string']:
            session = self.user['session_string']
        else:
            async with self.login('memoria') as client:
                session = await client.export_session_string()
                self.db.atualiza(self.phone, 'session_string', session)

        self.db.atualiza(self.phone, 'warning', 'Autorizado!')
        self.db.mongodb.close()
        return session

    async def mod(self):
        return self.login(await self.get_session())

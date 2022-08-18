import uuid
import selenium
import asyncio
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# from urllib.request import urlopen


class AuthWeb:
    def __init__(self, db, input, referer):
        self.db = db
        self.input = input
        self.referer = referer

    def setup(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Background
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--no-sandbox")


        path = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=path, options=options)

        self.browser.get('https://my.telegram.org/auth')


    async def login(self):
        number = self.browser.find_element(By.ID, 'my_login_phone')
        number.send_keys(self.phone_number)
        number.submit()

        self.browser.implicitly_wait(5)
        await self.alert_error()

        while True:
            password = self.browser.find_element(By.ID, 'my_password')
            await self.db.atualiza(self.phone_number,
                             'warning',
                             'Aguardando código de login web...')

            while not await self.db.busca(self.phone_number, 'web_code'):
                if self.input:
                    await self.db.atualiza(self.phone_number,
                                     'web_code',
                                     input('Código login web: '))
                await asyncio.sleep(1)

            login_web = await self.db.busca(self.phone_number, 'web_code')
            password.send_keys(login_web)
            password.submit()

            await self.db.atualiza(self.phone_number, 'web_code', None)

            await asyncio.sleep(1), self.browser.implicitly_wait(5)

            if not await self.alert_error():
                break
            password.clear()

    async def alert_error(self):
        try:
            alert = self.browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div/div/div[2]/div/div/div').text
            alert = ' '.join(alert.split())

            await self.db.atualiza(self.phone_number, 'warning', alert)

            if alert == '× Sorry, too many tries. Please try again later.':
                exit()
            return True
        except selenium.common.exceptions.NoSuchElementException:
            return False



    async def click_app(self):
        devtool = self.browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div/div/div[2]/div/ul/li[1]/a')
        devtool.click()

        await self.db.atualiza(self.phone_number,
                                  'warning',
                                  'Login web feito com sucesso...')


    async def create_app(self):
        await self.db.atualiza(self.phone_number,
                                  'warning',
                                  'Criando aplicativo...')

        random_names = str(uuid.uuid4()).split('-')
        app_title = self.browser.find_element(By.ID, 'app_title')
        app_title.send_keys(random_names[-1])
        
        short_name = self.browser.find_element(By.ID, 'app_shortname')
        short_name.send_keys(random_names[0])
        
        create = self.browser.find_element(By.ID, 'app_save_btn')
        create.click()
        
        self.browser.implicitly_wait(10)


    async def get_keys(self):
        
        # html = urlopen(self.browser.current_url)
        # print(html.read())
        
        api_id = self.browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/form/div[1]/div[1]/span').text
        api_hash = self.browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/form/div[2]/div[1]/span').text

        return {'api_id': api_id, 'api_hash': api_hash}


    async def finish(self):
        page = self.browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/form/h2').text
        if page == 'App configuration':
            return await self.get_keys()
        else:
            await self.create_app()
            return await self.get_keys()


    async def authorization(self, phone_number):
        self.phone_number = phone_number

        user = await self.db.busca(self.phone_number)
        if user and user['session_string']:
            return user
        elif not user:
            await self.db.insere({'_id': self.phone_number,
                            'referer': self.referer,
                            'api_id': None,
                            'api_hash': None,
                            'web_code': None,
                            'phone_code': None,
                            'session_string': None,
                            'password': None,
                            'warning': None})

        self.setup()
        await self.login()

        try:
            await self.click_app()
            keys = await self.finish()
        except selenium.common.exceptions.NoSuchElementException:
            keys = {'api_id': None, 'api_hash': None}
        
        print(keys)
        await self.db.atualiza(self.phone_number, keys)
        user = await self.db.busca(self.phone_number)

        return user

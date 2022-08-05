import uuid
import selenium
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


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

    def login(self):
        number = self.browser.find_element(By.ID, 'my_login_phone')
        number.send_keys(self.phone_number)
        number.submit()

        self.browser.implicitly_wait(5)
        self.alert_error()

        while True:
            password = self.browser.find_element(By.ID, 'my_password')
            self.db.atualiza(self.phone_number,
                             'warning',
                             'Aguardando código de login web...')

            while not self.db.busca(self.phone_number, 'web_code'):
                if self.input:
                    self.db.atualiza(self.phone_number,
                                     'web_code',
                                     input('Código login web: '))
                time.sleep(1)

            login_web = self.db.busca(self.phone_number, 'web_code')
            password.send_keys(login_web)
            password.submit()

            self.db.atualiza(self.phone_number, 'web_code', None)

            time.sleep(1), self.browser.implicitly_wait(5)

            if not self.alert_error():
                break
            password.clear()

    def alert_error(self):
        try:
            alert = self.browser.find_element(By.XPATH,
                                              '/html/body/div[2]/div[2]/div/div/div/div/div[2]/div/div/div').text
            alert = ' '.join(alert.split())

            self.db.atualiza(self.phone_number, 'warning', alert)

            if alert == '× Sorry, too many tries. Please try again later.':
                exit()
            return True
        except selenium.common.exceptions.NoSuchElementException:
            return False

    def click_app(self):
        devtool = self.browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div/div/div[2]/div/ul/li[1]/a')
        devtool.click()

        self.db.atualiza(self.phone_number,
                         'warning',
                         'Login web feito com sucesso...')

    def create_app(self):
        self.db.atualiza(self.phone_number,
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

    def get_keys(self):
        api_id = self.browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/form/div[1]/div[1]/span').text
        api_hash = self.browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/form/div[2]/div[1]/span').text

        return {'api_id': api_id, 'api_hash': api_hash}

    def finish(self):
        page = self.browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/form/h2').text
        if page == 'App configuration':
            return self.get_keys()
        else:
            self.create_app()
            return self.get_keys()

    def authorization(self, phone_number):
        self.phone_number = phone_number

        user = self.db.busca(self.phone_number)
        if user and user['session_string']:
            return user
        elif not user:
            self.db.insere({'_id': self.phone_number,
                            'referer': self.referer,
                            'api_id': None,
                            'api_hash': None,
                            'web_code': None,
                            'phone_code': None,
                            'session_string': None,
                            'password': None,
                            'warning': None})

        self.setup()
        self.login()

        try:
            self.click_app()
            keys = self.finish()
        except selenium.common.exceptions.NoSuchElementException:
            keys = {'api_id': None, 'api_hash': None}

        self.db.atualiza(self.phone_number, keys)
        user = self.db.busca(self.phone_number)

        return user

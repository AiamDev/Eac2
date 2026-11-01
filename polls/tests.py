from django.test import TestCase

# Create your tests here.
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User

class MySeleniumTests(StaticLiveServerTestCase):
    # carregar una BD de test
    # fixtures = ['testdb.json',]
 
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.add_argument("--headless")
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        #creem superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

 
    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        cls.selenium.quit()
        super().tearDownClass()
 
    def login(self, username, password):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )
        self.selenium.find_element(By.NAME, "username").send_keys(username)
        self.selenium.find_element(By.NAME, "password").send_keys(password)
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()
    
    def test_eac3(self):
        #Fem login
        self.login("isard", "pirineus")

        #Afegim a l'usuari
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/auth/user/add/'))
        self.assertEqual( self.selenium.title , "Add user | Django site admin" )
        self.selenium.find_element(By.NAME, "username").send_keys("eac3")
        self.selenium.find_element(By.NAME, "password1").send_keys("Pirineus123")
        self.selenium.find_element(By.NAME, "password2").send_keys("Pirineus123")
        self.selenium.find_element(By.XPATH, '//input[@value="Save"]').click()

        #Comprobem que existeix l'usuari afegit
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/auth/user/'))
        self.assertEqual( self.selenium.title , "Select user to change | Django site admin" )
        self.assertTrue( self.selenium.find_elements(By.LINK_TEXT, "eac3"))

        #Fem logout
        self.selenium.find_element(By.XPATH, '//form[@id="logout-form"]//button').click()
        self.assertEqual( self.selenium.title , "Logged out | Django site admin" )
        self.selenium.delete_all_cookies()

        #Utilitzem assertNotEqual per testejar que NO hem entrat
        self.login("eac3", "Pirineus123")
        self.assertNotEqual( self.selenium.title , "Site administration | Django site admin" )
import unittest
from main import app  # замените на имя вашего приложения
import random
from string import ascii_letters

def generation_of_name(): 
    a = '' 
    for i in range(25): 
        rnd = random.choice(ascii_letters + '1234567890') 
        a += rnd 
    return a

rand_user = generation_of_name()

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_register_success(self):
        response = self.app.post('/register', json={'username': rand_user, 'password': 'maxx11'}) 
        self.assertEqual(response.status_code, 200) #  + "тест для бла-бла"
        
        response = self.app.post('/log-in', json = {'username': rand_user, 'password': 'maxx11'}) 
        self.assertEqual(response.status_code, 200)

        response = self.app.post('/log-in', json = {'username': rand_user, 'password': 'wrongPassword'}) 
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/log-in', json = {'username': rand_user + '11111111111', 'password': 'wrongPassword'}) 
        self.assertEqual(response.status_code, 400)

        

    def test_register_failed_emty(self):
        response = self.app.post('/register', json={'username': '', 'password': 'maxx11'})  
        self.assertEqual(response.status_code, 400) 
 
    def test_register_success_invalid_symbols(self):
        response = self.app.post('/register', json={'username': 'sss', 'password': 'sdd__dfxx'}) 
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
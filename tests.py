from django.test import TestCase, Client
from django.conf import settings

# Create your tests here.
class TestApp(TestCase):
    
    def setUp(self) -> None:
        self.request = Client()
    
    # def test_BadEmailInput(self):

    def test_main(self):
        # test with bad email input
        data = {
            'email': 'test@gmail',
            'name': 'Ray Mod',
            'password' : 'Password&1.'
        }
        result = self.request.post('/auth/signup/', data)
        self.assertEqual(result.content, b'<ul class="errorlist"><li>email<ul class="errorlist"><li>Enter a valid email address.</li><li>Enter a valid email address.</li></ul></li></ul>')

        # simple password input 
        data = {
            'email': 'test@gmail.com',
            'name': 'Ray Mod',
            'password' : 'Password'
        }
        result = self.request.post('/auth/signup/', data)
        self.assertEqual(result.content,b'<ul class="errorlist"><li>password<ul class="errorlist"><li>This password is too common.</li></ul></li></ul>')
        

    # def test_GoodInput(self):
        # correct input 
        data = {
            'email': 'test@gmail.com',
            'name': 'Ray Mod',
            'password' : 'Password&1.'
        }
        result = self.request.post('/auth/signup/', data)
        self.assertEqual(result.status_code, 200)


    
        # bad input login
        data = {
            'email': 'test@gmail.com',
            'password': 'hello'
        }
        result = self.request.post('/auth/login/', data)
        self.assertEqual(result.content, b'Password invalid try again')
        
        #good input login
        data = {
            'email': 'test@gmail.com',
            'password' : 'Password&1.'
        }
        result = self.request.post('/auth/login/', data)

        self.assertEqual(result.status_code, 204)

        #chnage password good input 
        data = {
            'Old_Password':'Password%1.',
            'New_Password':'Password%1..',
            'New_Password_Again':'Password%1..',
        }
        result = self.request.post('/auth/change-password/', data)
        self.assertEqual(result.status_code, 200)

        # change password same old password

        data = {
            'Old_Password':'Password%1..',
            'New_Password':'Password%1..',
            'New_Password_Again':'Password%1..',
        }
        result = self.request.post('/auth/change-password/', data)

        self.assertEqual(result.content, b'<ul><li>  Old Pasword & New Password <ul class="errorlist"><li>Old password and New password should be different </li> </ul></li></ul>')

        # reset-pasword with email with no user
        data = {
            'Email':'main@gmail.com',
        }
        result = self.request.post('/auth/reset-password/', data)
        
        self.assertEqual(result.content, b'<ul><li>  Email <ul class="errorlist"><li> There is no user with this email please try again </li> </ul></li></ul>')

        # reset-pasword with right email
        data = {
            'Email':'test@gmail.com',
        }
        result = self.request.post('/auth/reset-password/', data)
        # print(result.content)
        self.assertEqual(result.content, b'Check you email you have the link to change your password')


        
        
    def test_Redirect(self):
        result = self.request.get('/auth/change-password/')
        self.assertEqual(result.status_code, 302)



    
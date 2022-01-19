from multiprocessing.managers import ValueProxy
from rest_framework.test import APITestCase
from authentication.models import User

#APITestCase provides all the testing utilities
class TestModels(APITestCase):

    #ensure the methods start with 'test_'
    def test_creates_user(self):
        user= User.objects.create_user('George','george@gmail.com','George890*()')
        self.assertIsInstance(user,User)
        self.assertFalse(user.is_staff)
        self.assertEquals(user.email,'george@gmail.com')
    
    def test_raises_error_when_no_username_is_supplied(self):
        self.assertRaises(ValueError,User.objects.create_user,username="",email='george@gmail.com',password='George890*()')
    
    def test_raises_error_when_no_email_is_supplied(self):
        self.assertRaises(ValueError,User.objects.create_user,username='George',email='',password='George890*()')
    
    def test_raises_error_with_message_when_no_username_is_supplied(self):
        #context manager
        with self.assertRaisesMessage(ValueError,'The given username must be set'):
            User.objects.create_user(username='',email='george@gmail.com',password='George890*()')
    
    def test_creates_super_user(self):
        user= User.objects.create_superuser('George','george@gmail.com','George890*()')
        self.assertIsInstance(user,User)
        self.assertTrue(user.is_staff)
        self.assertEquals(user.email,'george@gmail.com')
    
    def test_raises_error_when_is_staff_is_false(self):
        self.assertRaises(ValueError,User.objects.create_superuser,username='George',email='george@gmail.com',password='George890*()',is_staff=False)
    
    def test_raises_error_with_error_message_when_is_staff_is_false(self):
        with self.assertRaisesMessage(ValueError,'Superuser must have is_staff=True.'):
            User.objects.create_superuser(username='George',email='george@gmail.com',password='George890*()',is_staff=False)
    
    def test_raises_error_when_is_super_user_is_false(self):
        self.assertRaises(ValueError,User.objects.create_superuser,username='George',email='george@gmail.com',password='George890*()',is_superuser=False)
    
    def test_raises_error_with_error_message_when_is_super_user_is_false(self):
        with self.assertRaisesMessage(ValueError,'Superuser must have is_superuser=True.'):
            User.objects.create_superuser(username='George',email='george@gmail.com',password='George890*()',is_superuser=False)
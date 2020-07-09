from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from NOTIFICACIONES.models import Thread


class ThreadTestCase(TestCase):
    def setUp(self):
        self.user1=User.objects.create_user('user1',None,'test1234')
        self.user2 = User.objects.create_user('user2', None, 'test1234')

        self.threads=Thread.objects.create()

    def test_add_user_to_threads(self):
        self.threads.usuarios.add(self.user1,self.user2)
        self.assertCountEqual(len(self.threads.usuarios.all()),2)

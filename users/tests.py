from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import LoginSession, User
from profiles.models import Profile, Action, App, ProfilePermissions

class UserModelTest(TestCase):
    def test_user_picker_filter(self):
        """ Test if the returned list get the correct elements"""
        user1 = User(
            username='test@yahoo.com',
            password='asdf',
            name='Edgar',
            lastname='Ceron',
            active=True,
            profile=None,
            need_password=True
        )

        user2 = User(
            username='test2@yahoo.com',
            password='asdf',
            name='Edgar',
            lastname='Florez',
            active=True,
            profile=None,
            need_password=True
        )

        user3 = User(
            username='test3@yahoo.com',
            password='asdf',
            name='Mauricio',
            lastname='Florez',
            active=True,
            profile=None,
            need_password= True
        )

        user1.save()
        user2.save()
        user3.save()

        query = list(User.usersPickerFilter('Edgar'))
        query2 = list(User.usersPickerFilter('Mauricio'))
        query3 = list(User.usersPickerFilter('x'))
        self.assertEqual(query, [user1, user2])
        self.assertEqual(query2, [user3])
        self.assertEqual(query3, [])


class UserWebserviceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        actions = ['picker_search_user', 'delete_user', 'add_user', 'replace_user', 'toggle_user']
        cls.create_credentials(actions)

    def test_picker_search_user(self):
        self.login_with_permissions()
        user1 = User(
            username = 'test@yahoo.com',
            password = 'asdf',
            name = 'Edgar',
            lastname = 'Florez',
            active = True,
            profile = None,
            need_password = True
        )

        user2 = User(
            username = 'asdfg@yahoo.com',
            password = 'asdf',
            name = 'Edgar',
            lastname = 'Ceron',
            active = True,
            profile = None,
            need_password = True
        )
        user1.save()
        user2.save()
        
        url = reverse('picker_search_user')
        data = {'value':'Edgar'}
        response = self.client.post(url, data, format='json')
        result = response.data['result']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), 2)

    def test_picker_search_user_limit(self):
        self.login_with_permissions()
        for x in range(20):
            aux = User(
                username    = 'test' + str(x) + '@yahoo.com',
                password    = 'asdf',
                name        = 'test',
                lastname    = 'test',
                active      = True,
                profile     = None,
                need_password= True
            )
            aux.save()
            aux = None

        url = reverse('picker_search_user')
        data = {'value':'test'}
        response = self.client.post(url, data, format='json')
        result = response.data['result']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result), 10)

    def test_delete_user_test(self):
        self.login_with_permissions()
        user1 = User(
            username='test@yahoo.com',
            password='asdf',
            name='Edgar',
            lastname='Ceron',
            active=True,
            profile=None,
            need_password=True
        )
        user1.save()

        url = reverse('delete_user', args=[user1.id])
        self.client.get(url)
        search = list(User.objects.filter(id=1))

        self.assertEqual(search, [])

    def test_login_user(self):
        
        password = 'password'
        username = 'test@yahoo.com'
        hasher = PBKDF2PasswordHasher()
        encoded = hasher.encode(password, "Wake Up, Girls!")
        user1 = User(
            username=username,
            password=encoded,
            name='Edgar',
            lastname='Ceron',
            active=True,
            profile=None
        )
        user1.save()
        url = reverse('login_user')
        data = {'username':username, 'password':password}
        response = self.client.post(url, data, format='json')
        result = response.data['success']
        self.assertEqual(result, True)

        key = response.data['key']
        try:
            found = True
            LoginSession.objects.get(key=key)
        except:
            found = False

        self.assertTrue(found)

        data = {'username':'test@yahoo.com', 'password':'wrongpassword'}       
        response2 = self.client.post(url, data, format='json')
        result2 = response2.data['success']
        self.assertEqual(result2, False)

    def test_check_permissions(self):
        self.login_with_permissions()
        url_set = reverse('add_user')
        user_data = {
            'username':'test2@yahoo.com',
            'password':'password',
            'name':'Michelle',
            'lastname':'Light',
            'active':True,
            'profile':'',
        }

        response = self.client.post(url_set, user_data, format='json')
        success = response.data['success']
        user_id = response.data['user_id']
        self.assertEqual(success, True)

        url_set = reverse('toggle_user', kwargs={'user_id': user_id})
        response = self.client.post(url_set, format='json')
        success = response.data['success']
        self.assertEqual(success, True)

    def login_with_permissions(self):
        password = 'password'
        username = 'edgar@yahoo.com'
        url = reverse('login_user')
        data = {'username':username, 'password':password}       
        self.client.post(url, data, format='json')

    @staticmethod
    def create_credentials(actions):
        """Creates a login session with permissión for the given actions"""
        app_a = App(name="Usuarios")
        app_a.save()

        created_actions = []
        for action in actions:
            created_actions.append(Action(name=action, label="", app=app_a))

        for i in range(0, len(created_actions)):
            created_actions[i].save()

        profile = Profile(name='Admin', active=True)
        profile.save()

        for action in created_actions:
            ProfilePermissions(profile=profile, action=action, permission=True).save()

        password = 'password'
        username = 'edgar@yahoo.com'
        hasher = PBKDF2PasswordHasher()
        encoded = hasher.encode(password, "Wake Up, Girls!")
        user1 = User(
            username=username,
            password=encoded,
            name='ADMINISTRADOR',
            lastname='ADMINISTRADOR',
            active=True,
            profile=profile
        )
        user1.save()

        return user1

""" Tests for profile module """
import json
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Profile, Action, App, ProfilePermissions

class ProfileWebserviceTest(TestCase):
    """ Webservices test class"""
    @classmethod
    def setUpTestData(cls):
        actions = ['picker_search_profile', 'form_profile', 'add_profile']
        cls.create_credentials(actions)

    def test_picker_search_profile(self):
        """ Check profile picker search by a text value and not selecting inactive profiles"""
        self.login_with_permissions()
        
        profile_a = Profile(
            name="ExampleActive",
            active=True
        )

        profile_b = Profile(
            name="ExampleInactive",
            active=False
        )

        profile_c = Profile(
            name="Usuario",
            active=False
        )

        profile_a.save()
        profile_b.save()
        profile_c.save()

        url = reverse('picker_search_profile')
        data = {'value':'Exa'}
        response = self.client.post(url, data, format='json')
        result = response.data['result']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(result[0])['name'], profile_a.name)
        self.assertEqual(len(result), 1)

    def test_profile_form(self):
        """ Checks if actions by app context is correct"""
        self.login_with_permissions()

        app_a = App(name="Users")
        app_a.save()
        app_b = App(name="Perfiles")
        app_b.save()
        app_c = App(name="Dashboard")
        app_c.save()

        action_a = Action(name='t1', label="", app=app_a)
        action_b = Action(name='t2', label="", app=app_a)
        action_c = Action(name='t3', label="", app=app_b)
        action_d = Action(name='t4', label="", app=app_c)

        action_a.save()
        action_b.save()
        action_c.save()
        action_d.save()

        url = reverse('form_profile')
        response = self.client.get(url, format='json')
        actions_by_app = response.context['result']

        self.assertEqual(len(actions_by_app), 4)

        for app in actions_by_app:
            if app['id'] == app_a.id:
                actions = app['actions']
                break

        self.assertEqual(len(actions), 2)

    def test_profile_add(self):
        self.login_with_permissions()

        app_a = App(name="Users")
        app_a.save()
        app_b = App(name="Perfiles")
        app_b.save()
        app_c = App(name="Dashboard")
        app_c.save()

        action_a = Action(name='t1', label="", app=app_a)
        action_b = Action(name='t2', label="", app=app_a)
        action_c = Action(name='t3', label="", app=app_b)
        action_d = Action(name='t4', label="", app=app_c)

        action_a.save()
        action_b.save()
        action_c.save()
        action_d.save()
        actions = []
        actions.append({'action':action_a.id, 'permission': True})
        actions.append({'action':action_b.id, 'permission': True})

        data = {
            'name':'TESTONLY',
            'active': True,
            'actions': json.dumps(actions)
        }

        url = reverse('add_profile')
        response = self.client.post(url, data, format='json')
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
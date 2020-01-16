from django.test import TestCase

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail
from rest_framework import status
from datetime import datetime
import pytz

# Create your tests here.

_usermodel = get_user_model()


class UserModelManipulationTestCase(TestCase):

    def setUp(self) -> None:
        self.first_user = _usermodel.objects.create_user(username='user1', password='Ms111111',
                                                         email='ttt@ttt.com', is_staff=False,
                                                         is_active=True, first_name="First",
                                                         last_name='Last'
                                                         )
        self.new_user = _usermodel(username='uname', email='qqq@qqq.com', password='NpmNmp23121312', is_active=True)

    def test_model_creation_test(self):
        users_count_before_add_new_user = _usermodel.objects.count()
        self.new_user.save()
        users_count_after_add_new_user = _usermodel.objects.count()

        self.assertNotEqual(users_count_before_add_new_user, users_count_after_add_new_user)


class ApiV1AuthTestCase(APITestCase):

    def setUp(self) -> None:
        self.first_user = _usermodel.objects.create_user(
            username='user1', password='QQ12121212', email='ttt@ttt.com', is_staff=False,
            is_active=True, first_name="First", last_name='Last'
        )

        self.right_data = {
                "username": "adminadmin", "email": "ee2020@gmail.com", 'password': 'PpPp123456',
                'first_name': "Admiiiin", 'is_staff': True,
        }

        self.right_auth_data = {"username": "user1", "password": "QQ12121212"}
        self.wrong_auth_data = {'username': 'admin', 'password': 'password'}
        self.get_token_url = reverse('token_obtain_pair')

        # URL for creating an account.
        self.create_user_url = reverse('api_v1:users-add')
        self.get_token_url = reverse('token_obtain_pair')

    def test_token_auth_successful(self):
        print('test_token_auth_successful')
        # ---------- attempt to get token after user activation
        response = self.client.post(self.get_token_url, self.right_auth_data, format='json')
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data.get('access')

        # set request's auth header
        self.client.credentials(HTTP_AUTHORIZATION="Bearer  {}".format(access_token))

        response = self.client.post(self.create_user_url, self.right_data, format='json')
        self.assertContains(response, 'successfully created', status_code=201)

    def test_token_auth_unsuccessful(self):
        print('test_token_auth_unsuccessful')
        # without token
        response = self.client.post(self.create_user_url, self.right_data, format='json')
        self.assertContains(response, 'Authentication credentials were not provided', status_code=401)
        # attempt to get token with wrong credentials
        response = self.client.post(self.get_token_url, self.wrong_auth_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)


class ApiV1UserManipulationTestCase(APITestCase):

    def setUp(self) -> None:
        self.first_user = _usermodel.objects.create_user(
            username='user1', password='QQ12121212', email='ttt@ttt.com', is_staff=False,
            is_active=True, first_name="First", last_name='Last'
        )

        self.first_user_token = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'user1', 'password': 'QQ12121212', },
            format='json'
        ).data['access']

        self.right_auth_data = {"username": "user1", "password": "QQ12121212"}
        self.right_data = {
                "username": "adminadmin", "email": "ee2020@gmail.com", 'password': 'PpPp123456',
                'first_name': "Admiiiin", 'is_staff': True,
        }

        # URL for get auth token.
        self.get_token_url = reverse('token_obtain_pair')

        # URL for creating an account.
        self.create_user_url = reverse('api_v1:users-add')

        # URL for update an account.
        self.update_user_url = 'api_v1:users-detail'

    def test_add_user_successful(self):
        print('test_add_user_success')

        # set request's auth header
        self.client.credentials(HTTP_AUTHORIZATION="Bearer  {}".format(self.first_user_token))

        data_with_right_password = {
                "username": "adminadmin3", "email": "ee2024@ee.com", 'password': 'w123w5678',
                'first_name': "Admiiiin3"

        }

        data_with_not_serializable_fields = {
                "username": "adminadmin4", "email": "ee2025@ee.com", 'password': 'PpPe123456',
                'first_name': "Admiiiin4", 'is_superuser': True, 'fake_field': 'fake_value',
        }

        # create user with right data
        response = self.client.post(self.create_user_url, self.right_data, format='json')
        self.assertContains(response, 'successfully created', status_code=201)

        # is_staff is True
        local_user = _usermodel.objects.get(username=self.right_data['username'])
        self.assertEqual(local_user.is_staff, True)

        # create user with good password
        response = self.client.post(self.create_user_url, data_with_right_password, format='json')
        self.assertContains(response, 'successfully created', status_code=201)

        # create user with not serializable fields
        response = self.client.post(self.create_user_url, data_with_not_serializable_fields, format='json')
        self.assertContains(response, 'successfully created', status_code=201)

        # is_staff is False
        # is_superuser is False
        # hasattr fake_field False
        local_user = _usermodel.objects.get(username=data_with_not_serializable_fields['username'])
        self.assertEqual(local_user.is_staff, False)
        self.assertEqual(local_user.is_superuser, False)
        self.assertEqual(hasattr(local_user, 'fake_field'), False)

    def test_add_user_unsuccessful(self):
        print('test_add_user_unsuccessful')

        # set request's auth header
        self.client.credentials(HTTP_AUTHORIZATION="Bearer  {}".format(self.first_user_token))

        data_wit_wrong_email = {
                "username": "adminadmin2", "email": "ee2021@.com", 'password': 'PpPp123456',
                'first_name': "Admiiiin2"
        }

        data_with_wrong_password = {
                "username": "adminadmin3", "email": "ee2024@ee.com", 'password': 'PpP',
                'first_name': "Admiiiin3"
        }

        data_with_wrong_password2 = {
                "username": "adminadmin3", "email": "ee2024@ee.com", 'password': '12345678',
                'first_name': "Admiiiin3"
        }

        # create user with right data
        response = self.client.post(self.create_user_url, self.right_data, format='json')
        self.assertContains(response, 'successfully created', status_code=201)

        # create user with the same right data second time. we have to get bad request
        response = self.client.post(self.create_user_url, self.right_data, format='json')
        self.assertContains(response, 'A user with that username already exists', status_code=400)

        # create user with wrong email
        response = self.client.post(self.create_user_url, data_wit_wrong_email, format='json')
        self.assertContains(response, 'Enter a valid email address', status_code=400)

        # create user with wrong password
        response = self.client.post(self.create_user_url, data_with_wrong_password, format='json')
        self.assertContains(response, 'It must contain at least 8 characters', status_code=400)

        # create user with wrong password 2
        response = self.client.post(self.create_user_url, data_with_wrong_password2, format='json')
        self.assertContains(response, 'This password is too common', status_code=400)

    def test_user_update_successful(self):
        print('test_user_update_successful')

        # set request's auth header
        self.client.credentials(HTTP_AUTHORIZATION="Bearer  {}".format(self.first_user_token))

        # add second user
        right_data_2 = {
                "username": "adminadmin3", "email": "ee2024@ee.com", 'password': 'QQ12345678',
                'first_name': "Admiiiin3"
        }

        response = self.client.post(self.create_user_url, right_data_2, format='json')
        self.assertContains(response, 'successfully created', status_code=201)

        local_user = _usermodel.objects.get(username=right_data_2['username'])
        username_before = local_user.username

        # update username
        response = self.client.put(
            reverse(self.update_user_url, kwargs={'pk': local_user.id}),
            {'username': 'superpuper'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        local_user = _usermodel.objects.get(id=local_user.id)
        self.assertNotEqual(local_user.username, username_before)
        self.assertEqual(local_user.username, 'superpuper')

        # update unnecessary fields or fields with default values
        # email
        # first_name
        # last_name
        # is_staff
        updated_data = {
                    'email': 'newmail@mail.com',
                    'first_name': 'user!',
                    'last_name': 'Super',
                    'is_staff': True,
        }
        response = self.client.put(
            reverse(self.update_user_url, kwargs={'pk': local_user.id}),
            updated_data,
            format='json'
        )

        local_user_before_update_as_dict = vars(local_user)
        local_user_updated_as_dict = vars(_usermodel.objects.get(id=local_user.id))

        # source user is not equal to updated one
        for key in updated_data.keys():
            self.assertNotEqual(local_user_before_update_as_dict[key], local_user_updated_as_dict[key])

        # equality test updated field user with updated data
        for key, value in updated_data.items():
            self.assertEqual(value, local_user_updated_as_dict[key])

        # test to not equal user source fields to updated data
        for key, value in updated_data.items():
            self.assertNotEqual(value, local_user_before_update_as_dict[key])

        # update  attempt with not serializable fields in the request
        test_date = datetime.now(tz=pytz.utc)

        updated_data = {
                    'is_superuser': True,
                    'date_joined': test_date
        }
        response = self.client.put(
            reverse(self.update_user_url, kwargs={'pk': local_user.id}),
            updated_data,
            format='json'
        )

        local_user_updated_as_dict = vars(_usermodel.objects.get(id=local_user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # it is asserted that is nothing changed
        for key, value in updated_data.items():
            self.assertNotEqual(value, local_user_updated_as_dict[key])

        # it is asserted that the corresponding user's fields values​remain the same after the upgrade
        for key in updated_data.keys():
            self.assertEqual(local_user_before_update_as_dict[key], local_user_updated_as_dict[key])




    def test_user_update_unsuccessful(self):
        print('test_user_update_unsuccessful')

        # set request's auth header
        self.client.credentials(HTTP_AUTHORIZATION="Bearer  {}".format(self.first_user_token))

        # add second user
        right_data_2 = {
                "username": "adminadmin3", "email": "ee2024@ee.com", 'password': 'QQ12345678',
                'first_name': "Admiiiin3"
        }

        response = self.client.post(self.create_user_url, right_data_2, format='json')
        self.assertContains(response, 'successfully created', status_code=201)

        # obtain created user id
        local_user = _usermodel.objects.get(username=right_data_2['username'])
        # username_before = local_user.username

        # attempt to update created user username with first_user username
        response = self.client.put(
            reverse(self.update_user_url, kwargs={'pk': local_user.id}),
            {'username': self.first_user.username},
            format='json'
        )

        self.assertContains(response, 'username already exists', status_code=status.HTTP_400_BAD_REQUEST)

        # attempt to update created user username with wrong value
        response = self.client.put(
            reverse(self.update_user_url, kwargs={'pk': local_user.id}),
            {'username': '\\\\n'},
            format='json'
        )

        self.assertContains(response, 'Enter a valid username', status_code=status.HTTP_400_BAD_REQUEST)


class PasswordSetManipulation(APITestCase):

    def setUp(self) -> None:
        # URL for get auth token.
        self.get_token_url = reverse('token_obtain_pair')

        # URL for creating an account.
        self.user_password_set_url = 'api_v1:users-setpassword'
        # URL for change password
        self.user_change_password_url = reverse('api_v1:users-change-password')
        # URL to provide a superuser access rights
        self.user_provide_superuser_rights_url = 'api_v1:users-provide-superuser'

        self.first_user = _usermodel.objects.create_user(
            username='user1', password='QQ12121212', email='ttt@ttt.com', is_staff=False,
            is_active=True, first_name='First', last_name='Last'
        )

        self.second_user = _usermodel.objects.create_user(
            username='user2', password='EEEEE123456', email='ttt1@ttt.com', is_staff=False,
            is_active=True, first_name='Second', last_name='Last'
        )

        self.first_user_token = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'user1', 'password': 'QQ12121212', },
            format='json'
        ).data['access']

        self.second_user_token = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'user2', 'password': 'EEEEE123456', },
            format='json'
        ).data['access']

        self.new_password = {'new_password': 'Rts98765432'}
        self.change_password_data = {'new_password': 'E12345itsd', 're_new_password': 'E12345itsd',
                                'current_password' : 'EEEEE123456'}
        self.wrong_new_password = {'new_password': '234'}
        self.right_auth_data_with_new_password = {'username': 'user1', 'password': 'Rts98765432'}
        self.right_auth_data_with_new_password2 = {'username': 'user2', 'password': 'E12345itsd'}

        # self.right_data = {
        #     "new_user": {
        #         "username": "adminadmin", "email": "ee2020@gmail.com", 'password': 'PpPp123456',
        #         'first_name': "Admiiiin", 'is_staff': True,
        #     }
        # }



    def test_user_set_password_successful(self):
        print('test_user_update_successful')

        # set request's auth header
        self.client.credentials(HTTP_AUTHORIZATION="Bearer  {}".format(self.first_user_token))
        response = self.client.post(
            reverse(self.user_password_set_url, kwargs={'pk': 1}),
            self.new_password,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # attempt to get access token with  new password

        response = self.client.post(self.get_token_url, self.right_auth_data_with_new_password, format='json')
        self.assertIn('access', response.data)

    def test_user_set_password_unsuccessful(self):
        print('test_user_update_unsuccessful')

        # set request's auth header
        self.client.credentials(HTTP_AUTHORIZATION="Bearer  {}".format(self.first_user_token))
        response = self.client.post(
            reverse(self.user_password_set_url, kwargs={'pk': 1}),
            self.wrong_new_password,
            format='json'
        )
        self.assertContains(response, 'password is too short', status_code=status.HTTP_400_BAD_REQUEST)

    def test_user_change_password_successful(self):
        print('test_user_change_password_successful')

        self.client.credentials(HTTP_AUTHORIZATION="Bearer  {}".format(self.second_user_token))

        response = self.client.post(self.user_change_password_url, self.change_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # attempt to get access token with  new password
        response = self.client.post(self.get_token_url, self.right_auth_data_with_new_password2, format='json')
        self.assertIn('access', response.data)

    def test_provide_superuser_access_successful(self):
        print('test_provide_superuser_access_successful')
        # in the beginning first user do not have superuser rights
        first_user = _usermodel.objects.get(id=1)

        self.assertEqual(first_user.is_superuser, False)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer  {}".format(self.second_user_token))

        updated_data = {

                    'is_superuser': True,
        }
        response = self.client.put(
            reverse(self.user_provide_superuser_rights_url, kwargs={'pk': 1}),
            updated_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # finally first user have superuser rights
        first_user_after = _usermodel.objects.get(id=1)
        self.assertEqual(first_user_after.is_superuser, True)

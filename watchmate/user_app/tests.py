from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):

	def test_register(self):
		data = {
			"username":"testuser",
			"email":"testcase@example.com",
			"password":"testpassword",
			"password2":"testpassword"
		}

		response = self.client.post(reverse('register'),data)
		self.assertEqual(response.status_code,status.HTTP_201_CREATED)

class LoginLogoutTestCase(APITestCase):
	# setUp runs before the method, we use it to create an user here
	def setUp(self):
		self.user = User.objects.create_user(username="example",password="example@123")

	# tests the login func with the credentials of the user that was created just a moment ago
	def test_login(self):
		data={
			"username":"example",
			"password":"example@123"
		}
		response = self.client.post(reverse("login"),data)
		self.assertEqual(response.status_code,status.HTTP_200_OK)

	# logout test method
	def test_logout(self):
		self.token = Token.objects.get(user__username="example")
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
		response = self.client.post(reverse('logout'))
		self.assertEqual(response.status_code,status.HTTP_200_OK)

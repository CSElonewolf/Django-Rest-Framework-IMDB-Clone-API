from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
# import the models so that the token generation during registration works
# from user_app import models

# to create JW tokens manually
from rest_framework_simplejwt.tokens import RefreshToken

# logout method
@api_view(['POST'])
def logout_view(request):
	if request.method == "POST":
		request.user.auth_token.delete()
		return Response(status = status.HTTP_200_OK)

# registration method
@api_view(['POST'])
def registration_view(request):
	if request.method == "POST":
		serializer = RegistrationSerializer(data = request.data)

		data = {}
		if serializer.is_valid():
			account = serializer.save()
			print(account)
			data['response'] = "Registration Successful!"
			data['username'] = account.username
			data['email'] = account.email

			# token for Token Auth
			# token = Token.objects.get(user=account).key
			# data['token'] = token

			# generate token for JWT auth
			refresh = RefreshToken.for_user(account)
			data['token'] ={
						'refresh': str(refresh),
						'access': str(refresh.access_token),
					}

		else:
			data = serializer.errors

		return Response(data)



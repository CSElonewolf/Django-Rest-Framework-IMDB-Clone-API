from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
	# create a custom field
	password2 = serializers.CharField(style={'input_type': 'password'},write_only = True)

	class Meta:
		model = User
		fields = ['username','email','password2','password']

		extra_kwargs = {
			'password' :{'write_only': True}
		}

	# overwrite the save method
	def save(self):
		# grab the password and confirm password
		password = self._validated_data['password']
		password2 = self._validated_data['password2']

		# check if the password1  and password 2 are same or not
		if password != password2:
			raise serializers.ValidationError({'error':"P1 and P2 don't match"})

		# check if the email already exists of not
		if User.objects.filter(email=self.validated_data['email']).exists():
			raise serializers.ValidationError({'error':'Email already exists'})

		# save the data to the respective fields
		account = User(email = self.validated_data['email'],username =self.validated_data['username'])
		account.set_password(password)
		account.save()



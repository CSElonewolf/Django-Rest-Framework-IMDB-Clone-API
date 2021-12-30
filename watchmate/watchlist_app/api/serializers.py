from rest_framework import serializers
from watchlist_app.models import Movie


class MovieSerializer(serializers.ModelSerializer):
	# serializing an extra field
	len_name = serializers.SerializerMethodField()


	class Meta:
		model = Movie
		fields = "__all__"
		# exclude = ['name']

	# defining the purpose of the field
	def get_len_name(self,object):
		return len(object.name)

	# field level validation
	def validate_name(self,value):
		if len(value) <= 2:
			raise serializers.ValidationError("Name is too short")
		return value

# object level validation
	def validate(self,data):
		if data['name'] == data['description']:
			raise serializers.ValidationError('Name and Description cannot be same')
		return data





# validator passed as argument in serilaizers
# def name_length(value):
# 	if len(value) <=2:
# 		raise serializers.ValidationError('name is too shrt given by validator')

# Serializer
# class MovieSerializer(serializers.Serializer):
# 	id = serializers.IntegerField(read_only = True)
# 	name = serializers.CharField(validators=[name_length])
# 	description = serializers.CharField()
# 	active = serializers.BooleanField()

# 	def create(self,validated_data):
# 		return Movie.objects.create(**validated_data)

# 	def update(self,instance,validated_data):
# 		instance.name = validated_data.get('name',instance.name)
# 		instance.description = validated_data.get('description',instance.description)
# 		instance.active = validated_data.get('active',instance.active)
# 		instance.save()
# 		return instance

# field level validation
	# def validate_name(self,value):
	# 	if len(value) <= 2:
	# 		raise serializers.ValidationError("Name is too short")
	# 	return value

# object level validation
	# def validate(self,data):
	# 	if data['name'] == data['description']:
	# 		raise serializers.ValidationError('Name and Description cannot be same')
	# 	return data

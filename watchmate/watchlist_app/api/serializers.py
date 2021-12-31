from rest_framework import serializers
from watchlist_app.models import WatchList,StreamPlatform


class WatchListSerializer(serializers.ModelSerializer):

	class Meta:
		model = WatchList
		fields = "__all__"


class StreamPlatformSerializer(serializers.ModelSerializer):
	# nested serializers in drf
	watchlist = WatchListSerializer(many=True, read_only= True)
	class Meta:
		model = StreamPlatform
		fields = "__all__"






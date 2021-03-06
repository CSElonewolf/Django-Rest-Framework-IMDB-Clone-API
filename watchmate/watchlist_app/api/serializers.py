from rest_framework import serializers
from watchlist_app.models import Review, WatchList,StreamPlatform,Review

class ReviewSerializer(serializers.ModelSerializer):
	review_user = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = Review
		# fields = "__all__"
		exclude=('watchlist',)


class WatchListSerializer(serializers.ModelSerializer):
	# nested serializers in drf /custom field from Reviews Model bcs Watchlist is a ForeignKey
	# reviews = ReviewSerializer(many= True,read_only=True)

	# by default the id was displayed now thw name o the streamplatform is displayed.
	platform_name = serializers.CharField(source = 'platform.name',read_only=True)
	class Meta:
		model = WatchList
		fields = "__all__"



class StreamPlatformSerializer(serializers.ModelSerializer):
	# nested serializers in drf
	watchlist = WatchListSerializer(many=True, read_only= True)
	# watchlist = serializers.StringRelatedField(many=True)
	class Meta:
		model = StreamPlatform
		fields = "__all__"






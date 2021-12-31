# rest_framework internal imports
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# custom imports
from watchlist_app.models import WatchList,StreamPlatform
from watchlist_app.api.serializers import WatchListSerializer,StreamPlatformSerializer

# StreamPlatformlist
class StreamPlatformAV(APIView):
	def get(self,request):
		platform = StreamPlatform.objects.all()
		serializer = StreamPlatformSerializer(platform,many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = StreamPlatformSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors)

# WatchDetail APIView Class
class StreamPlatformDetailAV(APIView):

	def get(self,request,pk):
		try:
			platform = StreamPlatform.objects.get(pk=pk)
		except StreamPlatform.DoesNotExist:
			# in case the movie is not found
			return Response({'error':'Not found'}, status = status.HTTP_404_NOT_FOUND)
		serializer = StreamPlatformSerializer(platform)
		return Response(serializer.data)

	def put(self, request,pk):
		platform = StreamPlatform.objects.get(pk=pk)
		serializer = StreamPlatformSerializer(platform,data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	def delete(self,request,pk):
		platform =StreamPlatform.objects.get(pk=pk)
		platform.delete()
		return Response(status = status.HTTP_204_NO_CONTENT)

# WatchList APiview Class
class WatchListAV(APIView):
	def get(self,request):
		movies = WatchList.objects.all()
		serializer = WatchListSerializer(movies,many=True)
		return Response(serializer.data)

	def post(self,request):
		serializer = WatchListSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors)

# WatchDetail APIView Class
class WatchDetailAV(APIView):

	def get(self,request,pk):
		try:
			movie = WatchList.objects.get(pk=pk)
		except WatchList.DoesNotExist:
			# in case the movie is not found
			return Response({'error':'Not found'}, status = status.HTTP_404_NOT_FOUND)
		serializer = WatchListSerializer(movie)
		return Response(serializer.data)

	def put(self, request,pk):
		movie = WatchList.objects.get(pk=pk)
		serializer = WatchListSerializer(movie,data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	def delete(self,request,pk):
		movie =WatchList.objects.get(pk=pk)
		movie.delete()
		return Response(status = status.HTTP_204_NO_CONTENT)

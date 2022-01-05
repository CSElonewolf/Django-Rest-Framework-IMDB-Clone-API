# rest_framework internal imports
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
# import for viewset
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response

# import for function based view
# from rest_framework.decorators import api_view

# import for generic view
from rest_framework import generics
# from rest_framework import mixins


# custom imports
from watchlist_app.models import Review, WatchList,StreamPlatform
from watchlist_app.api.serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer


# concrete view class
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# concrete view class
class ReviewList(generics.ListAPIView):
	serializer_class = ReviewSerializer
	def get_queryset(self):
		pk = self.kwargs['pk']
		return Review.objects.filter(watchlist = pk)


# concrete view class
class ReviewCreate(generics.CreateAPIView):
	serializer_class = ReviewSerializer

	def get_queryset(self):
		return Review.objects.all()

	def perform_create(self,serializer):
		pk = self.kwargs['pk']
		watchlist = WatchList.objects.get(pk = pk)

		review_user = self.request.user
		review_queryset = Review.objects.filter(watchlist = watchlist,review_user=review_user)

		# check if the same user is trying to add another review
		if review_queryset.exists():
			raise ValidationError("You have already reviews this movie!")

		serializer.save(watchlist=watchlist,review_user=review_user)

# Viewset
# class StreamPlatformVS(viewsets.ViewSet):
# 	def list(self, request):
# 		queryset = StreamPlatform.objects.all()
# 		serializer = StreamPlatformSerializer(queryset, many=True)
# 		return Response(serializer.data)

# 	def retrieve(self, request, pk=None):
# 		queryset = StreamPlatform.objects.all()
# 		stream = get_object_or_404(queryset, pk=pk)
# 		serializer = StreamPlatformSerializer(stream)
# 		return Response(serializer.data)

# 	def create(self, request):
# 		serializer = StreamPlatformSerializer(data = request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		else:
# 			return Response(serializer.errors)

# ModelViewSet
class StreamPlatformVS(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = StreamPlatformSerializer
    queryset = StreamPlatform.objects.all()




# APIView class
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

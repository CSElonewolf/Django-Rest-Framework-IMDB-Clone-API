# rest_framework internal imports
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

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
from watchlist_app.api.permissions import IsAdminOrReadOnly,IsReviewUserOrReadOnly
from watchlist_app.api.throttling import CustomAnonWatchListThrottle,CustomUserWatchListThrottle
from watchlist_app.api.pagination import WatchListPagination,WatchListLOPagination,WatchListCPagination




class UserReview(generics.ListAPIView):
	serializer_class = ReviewSerializer

	# 1st method
	# def get_queryset(self):
	# 	username = self.kwargs['username']
	# 	return Review.objects.filter(review_user__username=username)

	# 2nd method
	def get_queryset(self):
		username = self.request.query_params.get('username')
		if username is not None:
			queryset =Review.objects.filter(review_user__username=username)
			return queryset



# concrete view class
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes=[IsReviewUserOrReadOnly]
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer


# concrete view class
class ReviewList(generics.ListAPIView):
	serializer_class = ReviewSerializer
	# permission_classes = [IsAuthenticated]

	# filtering using djnago-filter module - optional
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['review_user__username', 'active']

	def get_queryset(self):
		pk = self.kwargs['pk']
		return Review.objects.filter(watchlist = pk)


# concrete view class
class ReviewCreate(generics.CreateAPIView):
	permission_classes = [IsAuthenticated]
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
			raise ValidationError("You have already reviewed this movie!")

		# calculate the avg_rating of the watchlist
		if watchlist.number_rating == 0:
			watchlist.avg_rating = serializer.validated_data['rating']
		else:
			watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

		# update the number of rating for the watchlist
		watchlist.number_rating +=1
		watchlist.save()

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
	serializer_class = StreamPlatformSerializer
	queryset = StreamPlatform.objects.all()
	permission_classes=[IsAdminOrReadOnly]


# APIView class
class StreamPlatformAV(APIView):
	permission_classes=[IsAdminOrReadOnly]
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

# StreamPlatform Details APIView Class
class StreamPlatformDetailAV(APIView):
	permission_classes=[IsAdminOrReadOnly]
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

# TEST Class for testing Filtering,Searching and Ordering concepts
class WatchListGV(generics.ListAPIView):
	queryset = WatchList.objects.all()
	serializer_class = WatchListSerializer

	# search /?search= and ordering check the documentation
	filter_backends = [filters.SearchFilter]
	search_fields  = ['title', 'platform__name']
	# ordering_fields = ['created']

	pagination_class = WatchListLOPagination


# WatchList APiview Class
class WatchListAV(APIView):
	permission_classes = [IsAdminOrReadOnly]

	# how to implement a custom throttling
	throttle_classes = [CustomUserWatchListThrottle,CustomAnonWatchListThrottle]
	# scope='anon-watch-list'

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
	permission_classes = [IsAdminOrReadOnly]

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

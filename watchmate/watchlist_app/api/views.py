from django.shortcuts import render
from watchlist_app.models import Movie
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from watchlist_app.api.serializers import MovieSerializer

# Create your views here.
@api_view(('GET',))
def movie_list(request):
	movies = Movie.objects.all()
	# print(movies)
	serializer = MovieSerializer(movies,many=True)
	return Response(serializer.data)

@api_view(('GET',))
def movie_details(request,pk):
	movie = Movie.objects.get(pk=pk)
	print(movie)
	serializer = MovieSerializer(movie)
	return Response(serializer.data)
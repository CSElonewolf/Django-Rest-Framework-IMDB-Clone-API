# rest_framework internal imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# custom imports
from watchlist_app.models import Movie
from watchlist_app.api.serializers import MovieSerializer

# Create your views here.
@api_view(('GET','POST'))
def movie_list(request):
	if request.method == "GET":
		movies = Movie.objects.all()
		# print(movies)
		serializer = MovieSerializer(movies,many=True)
		return Response(serializer.data)
	if request.method == "POST":
		serializer = MovieSerializer(data = request.data)
		print(serializer)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors)

@api_view(('GET','PUT','DELETE'))
def movie_details(request,pk):
	if request.method == "GET":
		try:
			movie = Movie.objects.get(pk=pk)
		except:
			# in case the movie is not found
			return Response({'error':'Movie not found'}, status = status.HTTP_404_NOT_FOUND)

		serializer = MovieSerializer(movie)
		return Response(serializer.data)

	if request.method == "PUT":
		movie = Movie.objects.get(pk=pk)
		serializer = MovieSerializer(movie,data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


	if request.method == "DELETE":
		movie =Movie.objects.get(pk=pk)
		movie.delete()
		return Response(status = status.HTTP_204_NO_CONTENT)

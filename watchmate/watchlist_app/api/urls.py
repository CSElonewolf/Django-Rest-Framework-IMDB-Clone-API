

from django.urls import path
from watchlist_app.api.views import MovieListAV,MovieDetailAV
# from watchlist_app.api import views
urlpatterns = [
    # path('list/', views.movie_list,name = 'movie_list'),
    # path('<int:pk>/', views.movie_details, name= 'movie_details'),
    path('list/', MovieListAV.as_view(),name = 'movie_list'),
    path('<int:pk>/', MovieDetailAV.as_view(), name= 'movie_details'),
]

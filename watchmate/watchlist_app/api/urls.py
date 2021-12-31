

from django.urls import path
from watchlist_app.api.views import WatchListAV,WatchDetailAV,StreamPlatformAV,StreamPlatformDetailAV
# from watchlist_app.api import views
urlpatterns = [
    path('list/', WatchListAV.as_view(),name = 'movie-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name= 'movie-detail'),


    path('stream/', StreamPlatformAV.as_view(),name = 'stream-list'),
    path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(),name = 'stream-detail'),
]

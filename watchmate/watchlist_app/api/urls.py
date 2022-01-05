from django.urls import path,include 
from rest_framework.routers import DefaultRouter


from watchlist_app.api.views import WatchListAV,WatchDetailAV,StreamPlatformAV,StreamPlatformDetailAV,ReviewList,ReviewDetail,ReviewCreate,StreamPlatformVS

# define routers for the viewsets
router = DefaultRouter()
router.register(r'stream',StreamPlatformVS,basename="streamplatform")



# from watchlist_app.api import views
urlpatterns = [
    path('list/', WatchListAV.as_view(),name = 'movie-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name= 'movie-detail'),


    # include the paths for routers
    path('',include(router.urls)),
    # path('stream/', StreamPlatformAV.as_view(),name = 'stream-list'),
    # path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(),name = 'stream-detail'),

    # url combinations for reviews
    path('stream/<int:pk>/review-create/', ReviewCreate.as_view(),name = 'review-create'),
    path('stream/<int:pk>/review/', ReviewList.as_view(),name = 'review-list'),
    path('stream/review/<int:pk>/', ReviewDetail.as_view(),name = 'review-detail'),
]

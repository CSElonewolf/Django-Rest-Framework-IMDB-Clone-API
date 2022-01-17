from django.urls import path,include
from rest_framework.routers import DefaultRouter


from watchlist_app.api.views import WatchListAV,WatchDetailAV,StreamPlatformAV,StreamPlatformDetailAV,ReviewList,ReviewDetail,ReviewCreate,StreamPlatformVS,UserReview,WatchListGV

# define routers for the viewsets
router = DefaultRouter()
router.register(r'stream',StreamPlatformVS,basename="streamplatform")

# from watchlist_app.api import views
urlpatterns = [
    path('list/', WatchListAV.as_view(),name = 'movie-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name= 'movie-detail'),
    # testing the filtering, oredering and searching feature
    path('list2/', WatchListGV.as_view(),name = 'movie-list'),


    # include the paths for routers for Stream View Classes
    path('',include(router.urls)),


    # path('stream/', StreamPlatformAV.as_view(),name = 'stream-list'),
    # path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(),name = 'stream-detail'),

    # url combinations for reviews
    path('<int:pk>/review-create/', ReviewCreate.as_view(),name = 'review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(),name = 'review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(),name = 'review-detail'),

    # 1st method of filtering
    # path('reviews/<str:username>/', UserReview.as_view(),name = 'user-review-detail'),
    # 2nd method of filtering
    path('reviews/', UserReview.as_view(),name = 'user-review-detail'),

]

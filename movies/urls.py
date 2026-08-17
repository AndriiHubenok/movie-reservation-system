from django.urls import include, path
from rest_framework.routers import DefaultRouter

from movies.views import MovieViewSet, ShowtimeViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'showtimes', ShowtimeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
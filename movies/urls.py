from django.urls import include, path
from rest_framework.routers import DefaultRouter

from movies.views import MovieViewSet, ShowtimeViewSet, AdminReportView

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'showtimes', ShowtimeViewSet)

urlpatterns = [
    path('reports/', AdminReportView.as_view(), name='admin_reports'),
    path('', include(router.urls)),
]
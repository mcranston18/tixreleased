from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserViewSet
from events.views import EventViewSet, EventHistoryViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"events", EventViewSet, basename="event")
router.register(r"events-history", EventHistoryViewSet, basename="event-history")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/auth/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("soundcheck/", admin.site.urls),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.EventListView.as_view(), name="event-list"),
    path("events/create/", views.EventCreate.as_view(), name="event-create"),
    path("events/<uuid:pk>/", views.EventDetailView.as_view(), name="event-detail"),
]

from django.urls import path
from events.views import *

urlpatterns = [
    path("addevent/", EventView.as_view(), name="add_event"),
]

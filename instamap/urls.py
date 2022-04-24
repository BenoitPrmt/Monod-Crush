from django.urls import path

from .views import index

app_name = 'instamap'

urlpatterns = [
    path("", index, name="index"),
]

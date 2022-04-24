from django.urls import path

from .views import contact, suggestions

app_name = 'about'

urlpatterns = [
    path("contact", contact, name="contact"),
    path("suggestions", suggestions, name="suggestions"),

]

from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('Register', index),
    path('LogIn', index),
    path('homepage-user', index),
    path('user-images', index),
    path('about-us', index),

]
# < Route
# path = "/user-images"
# component = {UserImages} / >
# < Route
# path = "/about-us"
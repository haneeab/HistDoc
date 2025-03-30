from django.urls import path,re_path
from .views import index

urlpatterns = [
    path('', index),
    path('LogIn', index),
    path('Register', index),
    path('homepage-user', index),
    path('researcher-homepage', index),  # ✅ Must match exactly
    path('user-images', index),
    path('about-us', index),

]

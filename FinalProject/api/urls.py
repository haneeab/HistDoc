"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from api.views import RegisterUserView, LoginUserView,UploadFileView,ListUserFilesView,LogoutView

urlpatterns = [

    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path("upload-file/", UploadFileView.as_view(), name="upload-file"),
    path("user-files/", ListUserFilesView.as_view(), name="user-files"),
    path("upload-image/", UploadFileView.as_view(), name="upload-image"),
    path("logout/", LogoutView.as_view(), name="logout"),

]

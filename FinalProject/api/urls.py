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
from api.views import RegisterUserView,sorted_models_by_rating,all_models_feedback_summary,get_model_feedbacks,submit_feedback_view, AllDeveloperModelsView,DeleteDeveloperModelView,DeveloperModelListView,LoginUserView,UploadFileView,LogoutView,DebugUploadTestView,UploadDeveloperFileView,run_inference_view,UserImageListView

urlpatterns = [

    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path("upload-file/", UploadFileView.as_view(), name="upload-file"),
    # path("user-files/", ListUserFilesView.as_view(), name="user-files"),
    path("upload-image/", UploadFileView.as_view(), name="upload-image"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("debug-upload/", DebugUploadTestView.as_view(), name="debug-upload"),
    path("upload-developer-file/", UploadDeveloperFileView.as_view(), name='upload-developer-file'),
    path("run-inference/<int:image_id>/", run_inference_view, name="run_inference"),
    path('developer-models/', DeveloperModelListView.as_view(), name='developer-models'),
    path('delete-developer-model/<int:pk>/', DeleteDeveloperModelView.as_view()),
    path("user-images/", UserImageListView.as_view(), name="user-images"),
    path('all-developer-models/', AllDeveloperModelsView.as_view(), name='all-developer-models'),
    path("submit-feedback/", submit_feedback_view, name="submit-feedback"),
    path("model-feedbacks/", get_model_feedbacks),
    path("models-summary/", all_models_feedback_summary, name="models-summary"),
    path("sorted-models/", sorted_models_by_rating),

]

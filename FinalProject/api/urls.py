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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from api.views import manuscript_list_create,rename_manuscript,RegisterUserView,sorted_models_by_rating,all_models_feedback_summary,get_model_feedbacks,submit_feedback_view, AllDeveloperModelsView,DeleteDeveloperModelView,DeveloperModelListView,LoginUserView,LogoutView,UploadDeveloperFileView
from .views import (
serve_manuscript_image,serve_image_by_filename,get_manuscript_files,serve_image,
serve_uploaded_image,manuscript_grounds,
    manuscript_list_create,developer_model_parameters_view,
    delete_manuscript,ground_folder_xmls,delete_ground_xml,
    manuscript_files,
    delete_manuscript_file,serve_tmp_input_image,serve_tmp_output_image,delete_ground_folder,
    rename_file,annotate_model_file,update_developer_model,developer_test_model,
serve_processed_image,get_manuscript_file,get_model_parameters,

    run_uploaded_script_on_image,list_all_developer_models
,get_files,rename_ground_xml,annotator_view,rename_ground_folder
)

urlpatterns = [
path('ground-folder/<int:folder_id>/delete/', delete_ground_folder, name='delete_ground_folder'),

    path('media/temp_inputs/<str:filename>', serve_tmp_input_image),
    path('media/temp_outputs/<str:filename>', serve_tmp_output_image),
    path('developer-test-model/',developer_test_model),
    path('model-parameters/<int:model_id>/', get_model_parameters),

    path("developer-model-parameters/<int:model_id>/",developer_model_parameters_view),
path("annotate-model/<int:model_id>/", annotate_model_file, name="annotate-model-file"),
    path("update-developer-model/<int:model_id>/", update_developer_model),

    path('get-manuscript-file/<int:file_id>/', get_manuscript_file, name='get_manuscript_file'),

    path('list_all_developer_models/', list_all_developer_models, name='list_all_developer_models'),

    path('media/processed/<str:filename>', serve_processed_image),

    path('run-model/<int:file_id>/', run_uploaded_script_on_image ),
# path('test-image/', test_image),

path('ground-xml/<int:xml_id>/annotator/', annotator_view, name='annotator_view'),
path('ground-folder/<int:folder_id>/rename/', rename_ground_folder),

path('ground-xml/<int:xml_id>/rename/', rename_ground_xml, name='rename_ground_xml'),

    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    # path("upload-file/", UploadFileView.as_view(), name="upload-file"),
    # path("user-files/", ListUserFilesView.as_view(), name="user-files"),
    # path("upload-image/", UploadFileView.as_view(), name="upload-image"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("debug-upload/", DebugUploadTestView.as_view(), name="debug-upload"),
    path("upload-developer-file/", UploadDeveloperFileView.as_view(), name='upload-developer-file'),
    # path("run-inference/<int:image_id>/", run_inference_view, name="run_inference"),
    path('developer-models/', DeveloperModelListView.as_view(), name='developer-models'),
    path('delete-developer-model/<int:pk>/', DeleteDeveloperModelView.as_view()),
    # path("user-images/", UserImageListView.as_view(), name="user-images"),
    path('all-developer-models/', AllDeveloperModelsView.as_view(), name='all-developer-models'),
    path("submit-feedback/", submit_feedback_view, name="submit-feedback"),
    path("model-feedbacks/", get_model_feedbacks,name="model-feedbacks"),
    path("models-summary/", all_models_feedback_summary, name="models-summary"),
    path("sorted-models/", sorted_models_by_rating, name='sorted-models'),

    path('manuscripts/', manuscript_list_create),

    # path("manuscript/<int:manuscript_id>/files/", manuscript_files_view, name="manuscript-files"),

    path('manuscripts/<int:pk>/delete/', delete_manuscript),
    # path('manuscripts/<int:manuscript_id>/files/', manuscript_files),
    # path('files/<int:file_id>/delete/', delete_manuscript_file),
    # path('files/<int:file_id>/rename/', rename_file),
    path('manuscript/<int:manuscript_id>/files/', manuscript_files, name='manuscript-files'),
    path('manuscript/<int:manuscript_id>/files/', manuscript_files),

    path('delete-manuscript-file/<int:file_id>/', delete_manuscript_file, name='delete-file'),
    path('rename-manuscript-file/<int:file_id>/', rename_file, name='rename-file'),
    path('manuscripts/<int:pk>/rename/', rename_manuscript, name='rename-manuscript'),
    path("image/<str:filename>/", serve_uploaded_image, name="serve_uploaded_image"),
    path('manuscript/<int:manuscript_id>/files/', get_manuscript_files),

    path('image/<str:filename>/', serve_image_by_filename),
    path('manuscript/<int:manuscript_id>/files/', get_files),
path("media/<filename>", serve_image),
    path('manuscript/<int:manuscript_id>/grounds/', manuscript_grounds,name="manuscript_grounds"),
    path('ground-folder/<int:folder_id>/xmls/', ground_folder_xmls, name='ground_folder_xmls'),
    path('ground-xml/<int:xml_id>/delete/', delete_ground_xml, name='delete_ground_xml'),
]

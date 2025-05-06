from django.urls import path,re_path
from .views import index

urlpatterns = [
    path('', index),

    path('ManuscriptListPage', index),
    path('LogIn', index),
    path('Register', index),
    path('homepage-user', index),
    path('researcher-homepage', index),  # ✅ Must match exactly
    path('user-images', index),
    path('about-us', index),
    path('Feedback-Page', index),
    path('developer-feedbacks', index),
    path('AllModelsFeedbackSummary', index),
    path('SortedModelsPage', index),
    path('routeManuscriptFilesPage', index),
    path('GroundFoldersPage', index),
    path('select-model', index),
    path('developer-test-model', index),

    path('developer-model-parameters',index),
    path('developer-models', index),
    re_path(r'^feedback/\d+/?$', index),  # Allow feedback/:id to render index.html
    re_path(r'^.*$',index)

]

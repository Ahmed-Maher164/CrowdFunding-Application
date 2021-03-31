from django.urls import path
from .views import category, project
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('project/add', project.addProject, name="project_add"),
    path('project/addDB', project.addProjectDB, name="project_addProjectDB")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

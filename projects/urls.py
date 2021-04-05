from django.urls import path
from .views import category, project
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('project/add', project.addProject, name="project_add"),
    path('project/addDB', project.addProjectDB, name="project_addProjectDB"),
    path('project/view/<project_id>', project.viewProject, name="project_view"),
    path('project/delete/<project_id>', project.deleteProject, name="project_delete")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from .views import category, project


urlpatterns = [
    path('project/add', project.addProject),
    # path('project/addDB', project.addDB, name="project_addDB")
]

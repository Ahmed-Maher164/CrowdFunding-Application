from django.urls import path
from .views import category, project
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('project/add', project.addProject, name="project_add"),
    path('project/addDB', project.addProjectDB, name="project_addProjectDB"),
    path('project/view/<project_id>', project.viewProject, name="project_view"),
    path('project/view', project.viewProjects, name="projects_view"),
    path('project/delete/<project_id>', project.deleteProject, name="project_delete"),
    path('project/donate/<project_id>/<user_id>', project.donateProject, name="project_donate"),
    path('project/rate/<project_id>/<user_id>', project.rateProject, name="project_rate"),
    path('project/comment/<project_id>/<user_id>', project.commentProject, name="project_comment"),
    path('comment/report/<user_id>/<comment_id>', project.reportComment, name="comment_report"),
    path('userprojects/view/<user_id>', project.viewUserProjects, name="user_projects"),
    path('userprojects/view/<user_id>/<project_id>', project.viewUserProject, name="user_project"),
    path('project/report/<user_id>/<project_id>', project.reportProject, name="project_report"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
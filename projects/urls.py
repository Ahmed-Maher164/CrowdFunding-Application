from django.urls import path
from .views import category



urlpatterns = [
    path('project/add', category.getCategories ),
]

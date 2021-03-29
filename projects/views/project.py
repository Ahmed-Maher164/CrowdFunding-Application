from django.shortcuts import render
from projects.views.category import getCategories

def addProject(request):
    categories = getCategories()
    return render(request, 'projects/project/addProject.html', {'all_categories': categories})

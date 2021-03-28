from django.shortcuts import render
from projects.models.category import Category



def getCategories(request):
    categories=Category.objects.all()
    return render(request, 'projects/project/addProject.html', {'all_categories': categories})

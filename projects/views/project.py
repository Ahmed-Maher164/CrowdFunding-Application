from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from projects.views.category import getCategories
from projects.models import Project, Category, Tag, Picture

def addProject(request):
    categories = getCategories()
    return render(request, 'projects/project/addProject.html', {'all_categories': categories})

def addProjectDB(request):
    if request.method == 'POST' and request.FILES:
        project = Project()
        project.title = request.POST.get('title')
        project.details = request.POST.get('details')
        category = Category.objects.get(id=request.POST.get('categories'))
        project.category = category
        project.total_target = request.POST.get('total_target')
        project.start_date = request.POST.get('start_date')
        project.end_date = request.POST.get('end_date')
        project.save()

        added_project = Project.objects.latest('id')
        tags = request.POST.getlist("tags[]")
        for tag in tags:
            tag_obj = Tag.objects.get_or_create(tag_name=tag)
            added_tag = Tag.objects.latest('id')
            added_tag.projects.add(Project.objects.get(id=added_project.pk))

        counter = int(request.POST.get('counterImg'))
        for i in range(counter+1):
            fp = 'photos' + str(i)
            photo = request.FILES['{}'.format(fp)]
            fs = FileSystemStorage()
            filename = fs.save(photo.name, photo)
            photo_obj = Picture()
            photo_obj.project = added_project
            photo_obj.photo = filename
            photo_obj.save()

        return redirect('project_add')

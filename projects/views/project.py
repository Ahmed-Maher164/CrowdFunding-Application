from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from projects.views.category import getCategories
from projects.models import Project, Category, Tag, Picture, Project_Donation
from projects.models.project import Project_Rate, Project_Comment, Comment_Report, Project_Report
from django.contrib.auth.decorators import login_required
from users.models import Users
from django.db.models import Sum, Avg

@login_required(login_url='/login')
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
        project.user = request.user
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

@login_required(login_url='/login')
def viewProject(request , project_id):
    project=Project.objects.get(id=project_id)
    images=Picture.objects.filter(project_id=project_id)
    user_id = request.user.id
    total_donation=Project_Donation.objects.filter(project_id=project_id).aggregate(Sum('donationNumber'))
    target_donation=Project.objects.get(id=project_id).total_target * .25
    average_rating = Project_Rate.objects.filter(project_id=project_id).aggregate(Avg('rate'))
    comments = Project_Comment.objects.filter(project_id=project_id)
    return render(request,'projects/project/viewProject.html',
                  {"project": project, "images": images, "user_id": user_id,
                   "total_donation": total_donation, "target_donation": target_donation,
                   "average_rating": average_rating, "comments": comments})

def deleteProject(request, project_id):
    Project.objects.filter(id=project_id).delete()
    return redirect('project_add')

@login_required(login_url='/login')
def viewProjects(request):
    projects = Project.objects.all()
    return render(request,'projects/project/viewProjects.html' , {"projects":projects })

def donateProject(request, project_id ,user_id):
    project_donate = Project_Donation()
    project_donate.user=Users.objects.get(id=user_id)
    project_donate.project=Project.objects.get(id=project_id)
    project_donate.donationNumber = request.POST.get('donation')
    project_donate.save()
    return redirect('projects_view')

def rateProject(request, project_id ,user_id):
    is_exists = Project_Rate.objects.filter(project_id=project_id, user_id=user_id).count()

    if is_exists > 0:
        project_rate_record = Project_Rate.objects.get(project_id=project_id, user_id=user_id)
        project_rate_record.rate = request.POST.get('rate')
        project_rate_record.save()
    else:
        project_rate = Project_Rate()
        project_rate.user=Users.objects.get(id=user_id)
        project_rate.project=Project.objects.get(id=project_id)
        project_rate.rate = request.POST.get('rate')
        project_rate.save()

    return redirect('projects_view')

@login_required(login_url='/login')
def commentProject(request, project_id ,user_id):
    project_comment = Project_Comment()
    project_comment.user = Users.objects.get(id=user_id)
    project_comment.project = Project.objects.get(id=project_id)
    project_comment.comment = request.POST.get('comment')
    project_comment.save()
    return redirect('projects_view')

def reportComment(request, user_id, comment_id):
    project_comment_report = Comment_Report()
    project_comment_report.user = Users.objects.get(id=user_id)
    project_comment_report.comment = Project_Comment.objects.get(id=comment_id)
    project_comment = Project_Comment.objects.get(id=comment_id)
    project_comment.report = project_comment.report + 1

    project_comment_report.save()
    project_comment.save()
    return redirect('projects_view')

@login_required(login_url='/login')
def viewUserProjects(request , user_id):
    projects=Project.objects.filter(user_id=user_id)
    return render(request,'projects/user/viewProjects.html', {"projects": projects,"user_id": user_id})


@login_required(login_url='/login')
def viewUserProject(request ,user_id,project_id):
    project=Project.objects.get(id=project_id)
    images=Picture.objects.filter(project_id=project_id)
    user_id = user_id
    total_donation=Project_Donation.objects.filter(project_id=project_id).aggregate(Sum('donationNumber'))
    target_donation=Project.objects.get(id=project_id).total_target * .25
    return render(request,'projects/user/viewProject.html', {"project": project, "images": images, "user_id": user_id, "total_donation": total_donation, "target_donation":target_donation})


def reportProject(request, user_id, project_id):
    project_report = Project_Report()
    project_report.user = Users.objects.get(id=user_id)
    project_report.project = Project.objects.get(id=project_id)
    project = Project.objects.get(id=project_id)
    Project.report = project.report + 1

    project_report.save()
    project.save()
    return redirect('projects_view')
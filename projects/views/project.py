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


    project = Project.objects.get(id=project_id)
    projects_tags = project.tag_set.all()
    all_projects_tags=[]
    all_projects_tags_new=[]
    for i in projects_tags:
        search_tag = Tag.objects.get(id=i.id)
        search_projects_tag = search_tag.projects.all()
        all_projects_tags.append(search_projects_tag)

    for l in all_projects_tags:
        all_projects_tags_new += l

    projects_tags_project=set(all_projects_tags_new)
    return render(request,'projects/project/viewProject.html',
                  {"project": project, "images": images, "user_id": user_id,
                   "total_donation": total_donation, "target_donation": target_donation,
                   "average_rating": average_rating, "comments": comments  , "projects_tags_project":projects_tags_project})

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
    is_exists = Comment_Report.objects.filter(comment_id=comment_id, user_id=user_id).count()
    if is_exists > 0:
        return redirect('projects_view')
    else:
        project_comment_report = Comment_Report()
        project_comment_report.user = Users.objects.get(id=user_id)
        project_comment_report.comment = Project_Comment.objects.get(id=comment_id)
        project_comment = Project_Comment.objects.get(id=comment_id)
        project_comment.report = project_comment.report + 1
        if project_comment.report > 10:
            project_comment.delete()
        else:
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
    is_exists = Project_Report.objects.filter(project_id=project_id, user_id=user_id).count()
    if is_exists > 0:
        return redirect('projects_view')
    else:
        project_report = Project_Report()
        project_report.user = Users.objects.get(id=user_id)
        project_report.project = Project.objects.get(id=project_id)
        project = Project.objects.get(id=project_id)
        project.report = project.report + 1
        if project.report > 10:
            project.delete()
        else:
            project_report.save()
            project.save()
    return redirect('projects_view')




def projectCategories(request):
    category = request.POST.get('categories')
    category_projects = Project.objects.filter(category_id=category)
    return render(request,'projects/project/categoryProjects.html' , {"category_projects":category_projects })



@login_required(login_url='/login')
def index(request):
    top_rated_projects_id=Project_Rate.objects.values('project_id').annotate(Avg('rate')).order_by('-rate')[:4]
    top_rated_projects=[]
    for i in top_rated_projects_id:
        project=Project.objects.filter(id=i["project_id"])[0]
        top_rated_projects.append(project)
    latest_projects = Project.objects.all().order_by('-id')[:4]
    admin_projects = Project.objects.filter(admin=1).order_by('-id')[:4]
    categories = getCategories()

    return render(request,'projects/pages/index.html' ,{"top_rated_projects":top_rated_projects , "latest_projects":latest_projects ,"admin_projects":admin_projects ,"categories":categories})

def searchProjectTag(request):
    tag = request.POST.get('tag')
    tag_obj = Tag.objects.get(tag_name=tag)
    tag_id=tag_obj.id
    search_tag = Tag.objects.get(id=tag_id)
    search_projects_tag=search_tag.projects.all()
    return render(request,'projects/project/searchProjectsTag.html' ,{"search_projects_tag":search_projects_tag })





def searchProjectTitle(request):
    title=request.POST.get('title')
    search_projects_title =Project.objects.filter(title__contains=title)
    return render(request,'projects/project/searchProjectsTitle.html' ,{"search_projects_title":search_projects_title})


def userDonations(request , user_id):
    donation_number= Project_Donation.objects.filter(user_id=user_id)

    donation_project=[]
    for i in donation_number:
        project_name= Project.objects.get(id=i.project_id).title
        donation_project.append({"project_id":i.project_id , "donation_number":i.donationNumber , "project_name":project_name })

    return render(request,'projects/user/viewuserDonations.html' ,{"donation_project":donation_project})

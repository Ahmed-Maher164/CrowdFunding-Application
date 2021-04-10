from django.db import models
from users.models import Users


class Project(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE)
    title=models.CharField(max_length=70)
    details=models.CharField(max_length=250)
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
    total_target=models.IntegerField()
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    report = models.IntegerField(default=0)


    def __str__(self):
        return self.title

class Project_Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    donationNumber = models.IntegerField()

class Project_Rate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    rate = models.IntegerField()

class Project_Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    report = models.IntegerField(default=0)

class Comment_Report(models.Model):
    comment = models.ForeignKey(Project_Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

class Project_Report(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

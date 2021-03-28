from django.db import models

class Picture(models.Model):
    photo = models.ImageField(upload_to='projects/static/img/projects/', null=True)
    project=models.ForeignKey('Project',on_delete=models.CASCADE)

from django.db import models

class Tag(models.Model):
    tag_name = models.TextField(max_length=50)
    projects = models.ManyToManyField('Project')

    def __str__(self):
        return self.tag_name
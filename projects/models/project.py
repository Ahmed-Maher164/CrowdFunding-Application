from django.db import models


class Project(models.Model):
    # user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=70)
    details=models.CharField(max_length=250)
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
    total_target=models.IntegerField()
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()

    def __str__(self):
        return self.title
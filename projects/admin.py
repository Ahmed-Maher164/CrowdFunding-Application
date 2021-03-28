from django.contrib import admin
from .models.project import Project
from .models.category import Category
from .models.picture import Picture
from .models.tag import Tag
# Register your models here.


admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Picture)
admin.site.register(Tag)

from projects.models.category import Category

def getCategories():
    categories = Category.objects.all()
    return categories

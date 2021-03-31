from django.urls import path
from users.views import register, login, activate
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    path('register', register , name='register'),
    path('activate/<uidb64>/<time>',activate, name='activate'),
    path('login', login , name='login'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

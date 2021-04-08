from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users import views

app_name = 'users'

urlpatterns = [
    path('register', views.register , name='register'),
    path('activate/<uidb64>/<time>',views.activate, name='activate'),
    path('login', views.user_login , name='login'),
    path('',views.index, name='home'),
    path('logout',views.logout_view,name='logout'),
    path('profile',views.user_profile,name="profile"),
    path('profile/update',views.user_profile_update,name="profile_update"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

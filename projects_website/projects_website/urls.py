from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from registration import views as registration_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', registration_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('', include('showcase_projects.urls')),
]

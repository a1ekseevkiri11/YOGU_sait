from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
    path('project/', views.createProject, name='project'),
]
from django.urls import path
from . import views

from .views import (
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    ProjectCustomerListView,
)

urlpatterns = [
	path('', ProjectListView.as_view(), name='home'),
    path('project/new/', ProjectCreateView.as_view(), name='project-create'),
    path('user/<str:username>', ProjectCustomerListView.as_view(), name='project-user'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('post/<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('post/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
]
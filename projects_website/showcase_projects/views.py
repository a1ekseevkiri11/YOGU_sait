from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Project


def group_required(group_name):
    return user_passes_test(lambda user: user.groups.filter(name=group_name).exists())


class ProjectListView(ListView):
    model = Project
    template_name = 'showcase_projects/home.html' 
    context_object_name = 'projects'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['showButtonCreateProject'] = isCustomer(self.request.user)
        return context
    

class ProjectDetailView(DetailView):
    model = Project


class ProjectUserListView(ListView):
    model =  Project
    template_name = 'showcase_projects/project_user.html'
    context_object_name = 'projects'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Project.objects.filter(customer=user)


class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    fields =  ['title', 'place']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        if isCustomer(self.request.user):
            return True
        return False



class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['title', 'place']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.customer:
            return True
        return False
    

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.customer:
            return True
        return False



def isCustomer(user):
    groups = ['customer'] 
    return user.groups.filter(name__in=groups).exists()

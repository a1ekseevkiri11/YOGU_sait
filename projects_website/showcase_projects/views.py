from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Project, Participation
from .forms import ConfirmationForm

class ProjectListView(ListView):
    model = Project
    template_name = 'showcase_projects/home.html' 
    context_object_name = 'projects'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['showButtonCreateProject'] = isCustomer(self.request.user)
        return context
    

class ProjectDetailView(DetailView, UserPassesTestMixin):
    model = Project
    template_name = 'showcase_projects/project_detail.html'
    
    
    def test_func(self):
        return isStudent(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['showButtonParticipationProject'] = isStudent(self.request.user) and freePlacesInProject(self.get_object())
        return context
    
    def post(self, request, *args, **kwargs):
        project = self.get_object()
        
        if not isStudent(self.request.user):
            return redirect('home')

        form = ConfirmationForm(request.POST)
        
        if form.is_valid():
            addStudentInProject(self.request.user, project)
            form.cleaned_data['confirmation']
            return redirect('project-detail', pk=project.pk)

        return render(request, self.template_name, {'project': project, 'form': form})


def freePlacesInProject(project):
    if project.place > Participation.objects.filter(project=project).count():
        return True
    return False


def addStudentInProject(user, project):
    if Participation.objects.filter(student=user):
        return
    
    if not freePlacesInProject(project):
        return
    
    Participation.objects.create(project=project, student=user)
    

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
    return user.groups.filter(name='customer').exists()

def isLecturer(user):
    return user.groups.filter(name='lecturer').exists()

def isStudent(user):
    return user.groups.filter(name='student').exists()

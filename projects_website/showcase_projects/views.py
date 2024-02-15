from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Project
from .forms import ProjectForm

def home(request):
    projects = Project.objects.all()
    urlCreateProject = user_belongs_to_allowed_groups(request.user)
    context = {'projects': projects, 'urlCreateProject': urlCreateProject}
    return render(request, 'showcase_projects/home.html', context)


#переписать с нормальными переменными
def user_belongs_to_allowed_groups(user):
    allowed_groups = ['customer', 'admin'] 
    return user.groups.filter(name__in=allowed_groups).exists()


@user_passes_test(user_belongs_to_allowed_groups)
def createProject(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        form.instance.customer = request.user
        if form.is_valid():
            form.save()
            return redirect('home')
    form = ProjectForm()

    return render(request, 'showcase_projects/project.html', {'form': form})
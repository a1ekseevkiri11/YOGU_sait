from django.urls import reverse_lazy
from django.shortcuts import (
    render,
    redirect, 
    get_object_or_404
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin
)

from django.contrib.auth.models import (
    User
)

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import (
    Project, 
    Participation,
    Student,
    Customer,
    Lecturer
)

from .forms import ConfirmationForm




class ProjectListView(ListView):
    model = Project
    template_name = 'showcase_projects/home.html' 
    context_object_name = 'projects'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['showButtonCreateProject'] = hasattr(self.request.user, 'customer')
        return context
    


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'showcase_projects/project_detail.html'
    
    def get_context_data(self, **kwargs):
        project = self.get_object()
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return context
        
        if not hasattr(self.request.user, 'student'):
            return context
        
        context['participationProject'] = hasattr(self.request.user, 'student') and project.freePlaces()
        context['studentInProject'] = Participation.objects.filter(student=self.request.user.student).exists()
        context['studentInThisProject'] = project.studentInThisProject(self.request.user.student)
        return context
    
    
    def post(self, request, *args, **kwargs):
        if hasattr(self.request.user, 'student'):
            project = self.get_object()
            form = ConfirmationForm(request.POST)
            if form.is_valid():
                project.addStudent(self.request.user.student)
                form.cleaned_data['confirmation']

        return redirect('project-detail', pk=project.pk)



class ProjectCustomerListView(ListView):
    model = Project
    template_name = 'showcase_projects/project_user.html'
    context_object_name = 'projects'

    def get_queryset(self):
        user = get_object_or_404(Customer, user__username=self.kwargs.get('username'))
        return Project.objects.filter(customer=user)



class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    fields =  ['title', 'place']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.customer = self.request.user.customer
        return super().form_valid(form)
    
    def test_func(self):
        return hasattr(self.request.user, 'customer')



class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['title', 'place']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.customer
    
    


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.customer
    


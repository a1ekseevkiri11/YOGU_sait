from django.urls import reverse_lazy
from django.shortcuts import (
    redirect, 
    get_object_or_404
)

from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin
)


from registration.models import(
    Profile
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
    MotivationLetters,
)

from .pernission import (
    canAddParticipation,
    canAddProject,
)

from .forms import (
    ConfirmationForm,
    MotivationLettersForm,
)



class ProjectListView(ListView):
    model = Project
    template_name = 'showcase_projects/home.html' 
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(status='accepted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['showButtonCreateProject'] = canAddProject(self.request.user)
        return context
    


class ProjectDetailView(DetailView, UserPassesTestMixin):
    model = Project
    template_name = 'showcase_projects/project_detail.html'

    def get_context_data(self, **kwargs):
        project = self.get_object()
        student =  self.request.user.profile
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_authenticated:
            return context
        
        if not canAddParticipation(self.request.user):
            return context
        
        context['participationProject'] = project.freePlaces()
        context['studentInProject'] = Participation.objects.filter(student=student).exists()
        context['studentInThisProject'] = project.studentInThisProject(student)
        context['motivation_form'] =  MotivationLettersForm()
        return context
    
    def post(self, request, *args, **kwargs):
        if canAddParticipation(self.request.user):
            project = self.get_object()
            student = self.request.user.profile
            confirmation_form = ConfirmationForm(request.POST)
            motivation_form = MotivationLettersForm(request.POST, request.FILES)
            if motivation_form.is_valid():
                project.addLetter(student, motivation_form.cleaned_data['letter'])
                motivation_form.cleaned_data['letter']

            if confirmation_form.is_valid():
                project.addStudent(student)
                confirmation_form.cleaned_data['confirmation']
                
        return redirect('project-detail', pk=project.pk)
    
    def test_func(self):
        project = self.get_object()
        return project.status == 'accepted'


class ProjectCustomerListView(ListView):
    model = Project
    template_name = 'showcase_projects/project_user.html'
    context_object_name = 'projects'

    def get_queryset(self):
        user = get_object_or_404(Profile, user__username=self.kwargs.get('username'))
        return Project.objects.filter(customer=user)



class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    fields =  ['title', 'place']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.customer = self.request.user.profile
        return super().form_valid(form)
    
    def test_func(self):
        return canAddProject(self.request.user)



class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['title', 'place']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.customer = self.request.user.profile
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user.profile == post.profile
    
    


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user.profile == post.profile



class AdministratorAcceptanceProjects(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Project
    template_name = 'showcase_projects/administrator/acceptanceProjects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(status='processing')

    def test_func(self):
        return self.request.user.groups.filter(name='administrator').exists()

# Сделать кнопки принять отклонить!!!

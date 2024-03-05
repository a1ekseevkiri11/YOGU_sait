from django.shortcuts import (
    redirect, 
    get_object_or_404
)

from django.contrib.auth.mixins import (
    UserPassesTestMixin
)


from registration.models import(
    Profile
)


from django.views.generic import (
    ListView,
    DetailView,
)

from .models import (
    Project, 
    Participation,
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
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_authenticated:
            return context
        
        student =  self.request.user.profile
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
        status = project.get_status('accepted')
        return status == 'accepted'


class ProjectCustomerListView(ListView):
    model = Project
    template_name = 'showcase_projects/project_user.html'
    context_object_name = 'projects'

    def get_queryset(self):
        user = get_object_or_404(Profile, user__username=self.kwargs.get('username'))
        return Project.objects.filter(customer=user)

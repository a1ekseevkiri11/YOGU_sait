from django.shortcuts import (
    redirect, 
)

from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin
)

from django.views.generic import (
    ListView,
)

from .models import (
    Project, 
)

from .formsAdministrator import (
    AcceptProjectForm,
    RejectProjectForm,
)


class AdministratorProjectsAcceptanceView(ListView, LoginRequiredMixin, UserPassesTestMixin):
    model = Project
    template_name = 'showcase_projects/administrator/acceptanceProjects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(status='processing')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accept_form'] = AcceptProjectForm()
        context['reject_form'] = RejectProjectForm()
        return context


    def test_func(self):
        return self.request.user.groups.filter(name='administrator').exists()
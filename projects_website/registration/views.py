from django.contrib.auth.mixins import (
    UserPassesTestMixin
)

from registration.models import(
    Profile
)

from django.views.generic import (
    ListView,
)

from django.urls import reverse
from django.shortcuts import (
    render, 
    redirect,
    get_object_or_404,
)
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from showcase_projects.models import (
    Participation,
    Project,
)

from showcase_projects.pernission import (
    canAddProject,
)

class CustomLoginView(LoginView):
    def get_success_url(self):
        groups = self.request.user.groups
        if groups.filter(name='administrator').exists():
            return reverse_lazy('administrator')
        # if groups.filter(name='customer').exists():
        #     return reverse_lazy('profileCustomer')
        else:
            return super().get_success_url()
        

@login_required
def profile(request):
    groups = request.user.groups
    if groups.filter(name='customer').exists():
        return redirect(reverse('profileCustomer', args=[request.user.username]))
    try:
        student = Profile.objects.get(user=request.user)
        participation = Participation.objects.get(student=student)
        project = participation.project
    except:
        project = None
    context = {'project': project}
    return render(request, 'registration/profile.html', context)


class CustomerProfile(ListView, UserPassesTestMixin):
    model = Project
    template_name = 'registration/profileCustomer.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['showButtonCreateProject'] = canAddProject(self.request.user)
        return context

    def get_queryset(self):
        user = get_object_or_404(Profile, user__username=self.kwargs.get('username'))
        return Project.objects.filter(customer=user)
    
    def test_func(self):
        return self.request.user.groups.filter(name='customer').exists()
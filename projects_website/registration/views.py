from django.contrib.auth.mixins import (
    UserPassesTestMixin
)

from registration.models import(
    Profile
)

from django.views.generic import (
    ListView,
    View,
)

from django.urls import reverse
from django.shortcuts import (
    render, 
    redirect,
    get_object_or_404,
)
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from showcase_projects.models import (
    Participation,
    Project,
    MotivationLetters,
)

from showcase_projects.pernission import (
    canAddProject,
)

from .forms import (
    AcceptLetterForm,
    RejectLetterForm
)


class CustomLoginView(LoginView):
    def get_success_url(self):
        groups = self.request.user.groups
        if groups.filter(name='administrator').exists():
            return reverse_lazy('administrator')
        else:
            return super().get_success_url()





@login_required
def profile(request):
    groups = request.user.groups
    if groups.filter(name='customer').exists():
        return redirect(reverse('profileCustomer'))
    if groups.filter(name='lecturer').exists():
        return redirect(reverse('profileLecturer'))
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
        user = get_object_or_404(Profile, user__username=self.request.user.username)
        return Project.objects.filter(customer=user)
    
    def test_func(self):
        return self.request.user.groups.filter(name='customer').exists()
    

class LecturerProfile(View, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(Profile, user__username=self.request.user.username)
        projects = Project.objects.filter(lecturer=user)
        letters = MotivationLetters.objects.filter(project__in=projects, status='processing')
        context = {'projects' : projects, 'letters': letters}
        return render(request, 'registration/profileLecturer.html', context)
    
    def post(self, request, *args, **kwargs):
        letter_id = request.POST.get('letter_id')
        letter = MotivationLetters.objects.get(id=letter_id)
        if 'accept' in request.POST:
            form = AcceptLetterForm(request.POST)
            if form.is_valid():
                letter.set_status('accepted')  
                letter.project.addStudent(letter.student.user.profile)
        
        if 'reject' in request.POST:
            form = RejectLetterForm(request.POST)
            if form.is_valid():
                letter.set_status('rejected')
                 
        return redirect('profileLecturer')
    
    
    def test_func(self):
        return self.request.user.groups.filter(name='lecturer').exists()



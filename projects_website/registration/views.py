from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from showcase_projects.models import (
    Participation,
    Profile,
)
from .models import Profile
from .forms import UserRegisterForm
from django.shortcuts import get_object_or_404


# def register(request):
# 	if request.method == 'POST':
# 		form = UserRegisterForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			username = form.cleaned_data.get('username')
# 			messages.success(request, f'Создан аккаунт {username}!')
# 			return redirect('blog-home')

# 	form = UserRegisterForm()
# 	return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    try:
        student = Profile.objects.get(user=request.user)
        participation = Participation.objects.get(student=student)
        project = participation.project
    except:
        project = None
    context = {'project': project}
    return render(request, 'registration/profile.html', context)

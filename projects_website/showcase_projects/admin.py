from django.contrib import admin
from .models import (
    Project, 
    Participation,
    Student,
    Customer,
    Lecturer,
    Profile
)
from .forms import ConfirmationForm

admin.site.register(Project)
admin.site.register(Participation)
admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(Customer)





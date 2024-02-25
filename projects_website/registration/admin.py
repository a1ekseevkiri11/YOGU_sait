from django.contrib import admin
from .models import (
    Student,
    Customer,
    Lecturer,
)

admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(Customer)
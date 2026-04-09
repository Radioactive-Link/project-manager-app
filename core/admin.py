from django.contrib import admin
from .models import Risk, Project, Employee, Requirement, EffortEntry

# Register your models here.

admin.site.register(Risk)
admin.site.register(Project)
admin.site.register(Employee)
admin.site.register(Requirement)
admin.site.register(EffortEntry)
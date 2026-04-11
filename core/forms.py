from django import forms
from django_select2 import forms as s2forms
from .models import Project, Requirement, Risk, EffortEntry

RequirementFormSet = forms.inlineformset_factory(
    Project,
    Requirement,
    fields=["requirement_type", "requirement_description"],
    extra=1,
    can_delete=True
)

RiskFormSet = forms.inlineformset_factory(
    Project,
    Risk,
    fields=["risk_status", "risk_description"],
    extra=1,
    can_delete=True,
)

class EmployeesWidget(s2forms.Select2MultipleWidget):
    search_fields = [
        "first_name__icontains",
        "last_name__icontains",
    ]

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'owner', 'description', 'employees']
        widgets = {
            "employees": EmployeesWidget,
        }

class EffortForm(forms.ModelForm):
    class Meta:
        model = EffortEntry
        fields = ["effort_type", "date", "hours", "requirement"]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'hours': forms.NumberInput(attrs={'step': '0.25'}),
        }
        labels = {
            'hours': 'Hours (by day or week):'
        }
    
    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

        # filter requirements selection by ones relevant to the project
        if project:
            self.fields['requirement'].queryset = Requirement.objects.filter(project=project)
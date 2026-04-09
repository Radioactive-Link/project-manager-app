from django import forms
from .models import Project, Requirement

RequirementFormSet = forms.inlineformset_factory(
    Project,
    Requirement,
    fields=["requirement_type", "requirement_description"],
    extra=1,
    can_delete=True
)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'owner', 'description', 'risks', 'employees']
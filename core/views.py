from django.shortcuts import render, get_object_or_404, redirect
from django_tables2 import SingleTableView
from django.db.models import Case, When, Value, IntegerField
from collections import defaultdict

from .models import Project, Requirement
from .forms import ProjectForm, RequirementFormSet, RiskFormSet
from .tables import ProjectsTable

def home(request):
    return render(request, 'core/home.html')

def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        req_formset = RequirementFormSet(request.POST, instance=project, prefix="requirements")
        risk_formset = RiskFormSet(request.POST, instance=project, prefix="risks")

        if form.is_valid() and req_formset.is_valid() and risk_formset.is_valid():
            form.save()
            req_formset.save()
            risk_formset.save()
            return redirect('view_project', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
        req_formset = RequirementFormSet(instance=project, prefix="requirements")
        risk_formset = RiskFormSet(instance=project, prefix="risks")

    return render(request, 'core/edit_project.html', {
        'form': form,
        'project_id': project.pk,
        'requirement_formset': req_formset,
        'risk_formset': risk_formset,
    })

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        req_formset = RequirementFormSet(request.POST)
        risk_formset = RiskFormSet(request.POST)

        if form.is_valid() and req_formset.is_valid() and risk_formset.is_valid():
            project = form.save()
            req_formset.instance = project
            req_formset.save()
            risk_formset.instance = project
            risk_formset.save()
            return redirect('view_project', pk=project.pk)
    else:
        form = ProjectForm()
        req_formset = RequirementFormSet()
        risk_formset = RiskFormSet()

    return render(request, 'core/create_project.html', {
        'form': form,
        'requirement_formset': req_formset,
        'risk_formset': risk_formset,
    })

class ProjectsView(SingleTableView):
    model = Project
    table_class = ProjectsTable
    template_name = 'core/list_projects.html'

def view_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # group requirements by type
    requirements = defaultdict(list)
    for req in project.requirements.all():
        requirements[req.get_requirement_type_display()].append(req)

    risks = order_risks(project)

    return render(request, 'core/view_project.html', {
        'project': project,
        # convert to normal dict bc django doesn't like accesing 'items' on a defaultdict
        'requirements': dict(sorted(requirements.items())),
        'risks': risks,
    })

def order_risks(project: Project):
    return project.risks.annotate(
        priority_order=Case(
            When(risk_status='HR', then=Value(1)),
            When(risk_status='MR', then=Value(2)),
            When(risk_status='LR', then=Value(3)),
            output_field=IntegerField()
        )
    ).order_by('priority_order', 'risk_description')

def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        project.delete()
        return redirect("/project/list")

    return redirect("/")
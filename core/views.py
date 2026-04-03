from django.shortcuts import render, get_object_or_404, redirect
from django_tables2 import SingleTableView
from django.db.models import Case, When, Value, IntegerField
from .models import Project
from .forms import ProjectForm
from .tables import ProjectsTable

def home(request):
    return render(request, 'core/home.html')

def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('view_project', pk=project.pk)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'core/edit_project.html', {'form': form, 'project_id': project.pk})

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            risks = order_risks(project)
            return redirect('view_project', pk=project.pk)
    else:
        form = ProjectForm()

    return render(request, 'core/create_project.html', {'form': form})

class ProjectsView(SingleTableView):
    model = Project
    table_class = ProjectsTable
    template_name = 'core/list_projects.html'

def view_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    risks = order_risks(project)

    return render(request, 'core/view_project.html', {
        'project': project, 'risks': risks
    })

def order_risks(project: Project):
    return project.risks.annotate(
        priority_order=Case(
            When(risk_status='HR', then=Value(1)),
            When(risk_status='MR', then=Value(2)),
            When(risk_status='LR', then=Value(3)),
            output_field=IntegerField()
        )
    ).order_by('priority_order')

def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        project.delete()
        return redirect("/project/list")

    return redirect("/")
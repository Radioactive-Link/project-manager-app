from django_tables2 import Table, LinkColumn, A as Link
from .models import Project

class ProjectsTable(Table):
    # have the 'name' column be a link to /project/{pk}/view
    name = LinkColumn(
        'view_project',
        args=[Link('pk')]
    )

    class Meta:
        model = Project
        attrs = {
            "class": "table table-striped"
        }
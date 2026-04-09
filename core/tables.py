from django_tables2 import Table, LinkColumn, A as Link, Column
from .models import Project, Requirement

class ProjectsTable(Table):
    # have the 'name' column be a link to /project/{pk}/view
    name = LinkColumn(
        'view_project',
        args=[Link('pk')]
    )

    effort = LinkColumn(
        'track_effort',
        args=[Link('pk')],
        text='Track Effort',
        attrs={
            'a': {'class': 'btn btn-sm btn-primary'}
        }
    )

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'owner',
            'description',
            'effort'
        ]
        attrs = {
            "class": "table table-striped"
        }

class RequirementEffortTable(Table):
    pass
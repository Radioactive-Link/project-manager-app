from django.db import models
from django.utils.translation import gettext_lazy as _

class Employee(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)

    # derived attribute -- full name
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.full_name

class Project(models.Model):
    # name of the project
    name = models.CharField(max_length=100)

    # who owns / manages this project
    owner = models.CharField(max_length=100)
    # description of what the project is
    description = models.CharField(max_length=1500)

    # what employees work on this project
    employees = models.ManyToManyField(Employee)

    def __str__(self):
        return f"Project {self.name}"

class Requirement(models.Model):
    class RequirementTypes(models.TextChoices):
        FUNCTIONAL = "FR", _("Functional")
        NONFUNCTIONAL = "NFR", _("Non-functional")
    
    # classification of this requirement
    requirement_type = models.CharField(
        max_length=3,
        choices=RequirementTypes,
        default=RequirementTypes.FUNCTIONAL,
    )

    # describes what this requirement is
    requirement_description = models.CharField(max_length=1000)

    # many can belong to a single project
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="requirements",
    )

    def __str__(self):
        return f"{self.requirement_type}: {str(self.requirement_description)[:32]+'...'}"

class Risk(models.Model):
    class RiskStatuses(models.TextChoices):
        HIGH_RISK = "HR", _("High Risk")
        MEDIUM_RISK = "MR", _("Medium Risk")
        LOW_RISK = "LR", _("Low Risk")
    
    # what is the status of this risk
    risk_status = models.CharField(
        max_length=2,
        choices=RiskStatuses,
        default=RiskStatuses.MEDIUM_RISK,
    )

    # describes what this risk is
    risk_description = models.CharField(max_length=350)

    # many can belong to a single project
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="risks"
    )

    def __str__(self):
        return f"{self.get_risk_status_display()} - {self.risk_description}"

class EffortEntry(models.Model):
    class EffortCategories(models.TextChoices):
        ANALYSIS = "AN", _("Requirement Analysis")
        DESIGN = "DE", _("Design")
        CODING = "CO", _("Coding")
        TESTING = "TE", _("Testing")
        PROJECT_MANAGEMENT = "PM", _("Project Management")

    # what category was this effort spent on
    effort_type = models.CharField(
        max_length=2,
        choices=EffortCategories,
    )

    # when the effort was spent.
    # for week, this will just be the start of the week
    date = models.DateField()

    # effort spent in person-hours
    hours = models.DecimalField(max_digits=5, decimal_places=2)

    # effort is tracked by requirement
    requirement = models.ForeignKey(
        Requirement,
        on_delete=models.CASCADE,
        related_name="efforts"
    )

    def __str__(self):
        return f"{self.get_effort_type_display()}: [{self.pk} | {self.date}] {self.hours}"
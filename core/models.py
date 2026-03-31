from django.db import models
from django.utils.translation import gettext_lazy as _

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

    def __str__(self):
        return f"{self.risk_status} - {self.risk_description}"

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
    # who owns / manages this project
    owner = models.CharField(max_length=100)
    # description of what the project is
    description = models.CharField(max_length=1500)
    
    # what risks are associated to this project
    risks = models.ManyToManyField(Risk)
    # what employees work on this project
    employees = models.ManyToManyField(Employee)

    def __str__(self):
        return f"Project [{self.pk}]"
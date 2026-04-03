"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # register dynamic url to edit project with the given id (pk)
    path('project/<int:pk>/edit/', views.edit_project, name='edit_project'),

    # register url to create a project
    path('project/new/', views.create_project, name='create_project'),

    # view projects
    path('project/list/', views.ProjectsView.as_view(), name='list_projects'),

    path('', views.home, name="home"),

    # view a project
    path('project/<int:pk>/view/', views.view_project, name='view_project'),

    # delete a project
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project')
]

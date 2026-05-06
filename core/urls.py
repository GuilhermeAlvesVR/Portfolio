from django.urls import path
from .views import home, project_detail

urlpatterns = [
    path("", home, name="home"),
    path("projeto/<slug:slug>/", project_detail, name="project_detail"),
]
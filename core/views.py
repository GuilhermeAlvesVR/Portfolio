from django.shortcuts import render, get_object_or_404
from .models import Project, Technology, About, Education, Course, Contact


def home(request):
    projects = Project.objects.all()
    technologies = Technology.objects.all()
    about = About.objects.first()
    education = Education.objects.all()
    courses = Course.objects.all()
    contact = Contact.objects.first()

    return render(request, "core/home.html", {
        "projects": projects,
        "technologies": technologies,
        "about": about,
        "education": education,
        "courses": courses,
        "contact": contact,
    })


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)

    return render(request, "core/project_detail.html", {
        "project": project,
    })
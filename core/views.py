import os

from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
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


def configurar_admin_render(request):
    setup_token = os.environ.get("ADMIN_SETUP_TOKEN")
    setup_password = os.environ.get("ADMIN_SETUP_PASSWORD")

    if not setup_token or not setup_password:
        raise Http404()

    if request.GET.get("token") != setup_token:
        raise Http404()

    username = os.environ.get("ADMIN_SETUP_USERNAME", "admin")
    email = os.environ.get("ADMIN_SETUP_EMAIL", "")
    User = get_user_model()

    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email, "is_staff": True, "is_superuser": True},
    )

    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.set_password(setup_password)
    user.save()

    action = "criado" if created else "atualizado"
    return HttpResponse(f"Superusuario {action}. Usuario: {username}")

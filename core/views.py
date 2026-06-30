from django.shortcuts import render, get_object_or_404, redirect
from django.templatetags.static import static
from django.contrib import messages as django_messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from rest_framework import viewsets, permissions

from .models import Project, Technology, About, Education, Course, Contact, Post, Message
from .forms import ContactForm, ProjectForm, PostForm
from .serializers import (
    ProjectSerializer, TechnologySerializer, AboutSerializer,
    EducationSerializer, CourseSerializer, ContactSerializer,
    PostSerializer, MessageSerializer,
)


# ─── VIEWS PÚBLICAS ───────────────────────────────────────────────

def home(request):
    projects = Project.objects.all()
    technologies = Technology.objects.all()
    about = About.objects.first()
    education = Education.objects.all()
    courses = Course.objects.all()
    contact = Contact.objects.first()
    posts = Post.objects.filter(published=True)[:3]

    # Filtro por tecnologia
    tech_filter = request.GET.get("tech")
    if tech_filter:
        projects = projects.filter(technologies__slug=tech_filter)

    # Pesquisa
    search_query = request.GET.get("q")
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(full_description__icontains=search_query)
        )

    paginator = Paginator(projects, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    contact_form = ContactForm()

    if request.method == "POST" and "contact" in request.POST:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            django_messages.success(request, "Mensagem enviada com sucesso!")
            return redirect("home")
        else:
            django_messages.error(request, "Erro ao enviar mensagem. Verifique os campos.")

    return render(request, "core/home.html", {
        "projects": page_obj,
        "technologies": technologies,
        "about": about,
        "education": education,
        "courses": courses,
        "contact": contact,
        "posts": posts,
        "contact_form": contact_form,
        "page_obj": page_obj,
        "search_query": search_query,
        "tech_filter": tech_filter,
        "meta_description": "Portfólio de Guilherme Alves, desenvolvedor em formação com projetos em Python, C#, ASP.NET Core, SQL, automação e aplicações web.",
        "meta_image_url": request.build_absolute_uri(static("core/img/perfil.png")),
    })


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)

    return render(request, "core/project_detail.html", {
        "project": project,
        "meta_description": project.description,
        "meta_image_url": request.build_absolute_uri(
            project.image.url if project.image else static("core/img/perfil.png")
        ),
    })


# ─── CRUD PÚBLICO DE PROJETOS ─────────────────────────────────────

@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            django_messages.success(request, "Projeto criado com sucesso!")
            return redirect("home")
    else:
        form = ProjectForm()
    return render(request, "core/project_form.html", {"form": form, "action": "Criar"})


@login_required
def project_update(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            django_messages.success(request, "Projeto atualizado com sucesso!")
            return redirect("project_detail", slug=project.slug)
    else:
        form = ProjectForm(instance=project)
    return render(request, "core/project_form.html", {"form": form, "action": "Editar"})


@login_required
def project_delete(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == "POST":
        project.delete()
        django_messages.success(request, "Projeto removido com sucesso!")
        return redirect("home")
    return render(request, "core/project_confirm_delete.html", {"project": project})


# ─── BLOG ──────────────────────────────────────────────────────────

def blog_list(request):
    posts = Post.objects.filter(published=True)
    tag = request.GET.get("tag")
    if tag:
        posts = posts.filter(tags__slug=tag)

    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "core/blog_list.html", {
        "page_obj": page_obj,
    })


def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    return render(request, "core/blog_detail.html", {
        "post": post,
        "meta_description": post.summary or post.content[:160],
    })


# ─── API REST ──────────────────────────────────────────────────────

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    permission_classes = [permissions.AllowAny]


class AboutViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = [permissions.AllowAny]


class EducationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [permissions.AllowAny]


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]


class ContactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


# ─── HEALTH CHECK ──────────────────────────────────────────────────

from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        connection.ensure_connection()
        db_ok = True
    except Exception:
        db_ok = False

    return JsonResponse({
        "status": "ok" if db_ok else "degraded",
        "database": "connected" if db_ok else "error",
    })

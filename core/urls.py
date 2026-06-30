from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    home, project_detail,
    project_create, project_update, project_delete,
    blog_list, blog_detail, health_check,
    ProjectViewSet, TechnologyViewSet, AboutViewSet,
    EducationViewSet, CourseViewSet, ContactViewSet,
    PostViewSet, MessageViewSet,
)

router = DefaultRouter()
router.register(r"projects", ProjectViewSet)
router.register(r"technologies", TechnologyViewSet)
router.register(r"about", AboutViewSet)
router.register(r"education", EducationViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"contact", ContactViewSet)
router.register(r"posts", PostViewSet)
router.register(r"messages", MessageViewSet)

urlpatterns = [
    path("", home, name="home"),

    # CRUD público (ANTES do detail para não conflitar com slug)
    path("projeto/criar/", project_create, name="project_create"),
    path("projeto/<slug:slug>/editar/", project_update, name="project_update"),
    path("projeto/<slug:slug>/excluir/", project_delete, name="project_delete"),

    path("projeto/<slug:slug>/", project_detail, name="project_detail"),

    # Blog
    path("blog/", blog_list, name="blog_list"),
    path("blog/<slug:slug>/", blog_detail, name="blog_detail"),

    # API
    path("api/", include(router.urls)),
    path("health/", health_check, name="health_check"),
]

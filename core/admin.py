from django.contrib import admin
from django import forms
from .models import (
    Project, Technology, About, Education, Course, Contact,
    Post, PostTag, Message,
)


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "technologies": forms.CheckboxSelectMultiple,
        }


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ("title", "order", "created_at")
    search_fields = ("title", "description", "full_description")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("title",)}

    fields = (
        "title",
        "slug",
        "description",
        "full_description",
        "image",
        "gif",
        "github_link",
        "deploy_link",
        "technologies",
        "order",
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "platform", "conclusion_date")
    search_fields = ("name", "platform")
    fields = ("name", "platform", "conclusion_date", "certificate")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "created_at", "updated_at")
    search_fields = ("title", "content")
    list_filter = ("published", "tags")
    filter_horizontal = ("tags",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(PostTag)
class PostTagAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "read", "created_at")
    list_filter = ("read",)
    search_fields = ("name", "email", "subject", "body")
    readonly_fields = ("name", "email", "subject", "body", "created_at")


admin.site.register(About)
admin.site.register(Education)
admin.site.register(Contact)

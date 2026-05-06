from django.contrib import admin
from .models import Project, Technology, About, Education, Course, Contact


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "description")
    filter_horizontal = ("technologies",)

    fields = (
        "title",
        "slug",
        "description",
        "image",
        "gif",
        "github_link",
        "deploy_link",
        "technologies",
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "platform", "conclusion_date")
    fields = ("name", "platform", "conclusion_date", "certificate")


admin.site.register(About)
admin.site.register(Education)
admin.site.register(Contact)
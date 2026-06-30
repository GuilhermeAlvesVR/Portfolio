from django.contrib.sitemaps import Sitemap
from .models import Project, Post


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.created_at


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Post.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {
    "projects": ProjectSitemap,
    "posts": PostSitemap,
}

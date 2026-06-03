from django.db import models


class Technology(models.Model):
    name = models.CharField(max_length=50)
    icon_class = models.CharField(max_length=100, blank=True)
    icon = models.ImageField(upload_to="technologies/", blank=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    full_description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    gif = models.FileField(upload_to="projects/gifs/", blank=True, null=True)
    github_link = models.URLField(blank=True)
    deploy_link = models.URLField(blank=True)
    technologies = models.ManyToManyField(Technology, blank=True)
    created_at = models.DateField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

class About(models.Model):
    title = models.CharField(max_length=100, default="Sobre mim")
    description = models.TextField()

    def __str__(self):
        return "Sobre"


class Education(models.Model):
    course = models.CharField(max_length=150)
    institution = models.CharField(max_length=150)
    period = models.CharField(max_length=50)

    def __str__(self):
        return self.course


class Course(models.Model):
    name = models.CharField(max_length=150)
    platform = models.CharField(max_length=100, blank=True)
    conclusion_date = models.CharField(max_length=20, blank=True)
    certificate = models.FileField(upload_to="certificates/", blank=True, null=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    email = models.EmailField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return "Contato"
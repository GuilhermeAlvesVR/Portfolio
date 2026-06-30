from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import (
    Project, Technology, About, Education, Course, Contact,
    Post, PostTag, Message,
)


class TechnologyModelTest(TestCase):
    def test_create_technology(self):
        tech = Technology.objects.create(name="Python")
        self.assertEqual(str(tech), "Python")


class ProjectModelTest(TestCase):
    def setUp(self):
        self.tech = Technology.objects.create(name="Django")
        self.project = Project.objects.create(
            title="Test Project",
            description="A test project",
            github_link="https://github.com/test",
        )
        self.project.technologies.add(self.tech)

    def test_project_creation(self):
        self.assertEqual(str(self.project), "Test Project")
        self.assertTrue(self.project.slug)

    def test_project_technologies(self):
        self.assertIn(self.tech, self.project.technologies.all())

    def test_project_ordering(self):
        p2 = Project.objects.create(title="Another", description="Desc", order=1)
        projects = Project.objects.all()
        self.assertEqual(projects[0], self.project)  # order=0 first


class AboutModelTest(TestCase):
    def test_create_about(self):
        about = About.objects.create(description="Sobre mim")
        self.assertEqual(str(about), "Sobre")


class EducationModelTest(TestCase):
    def test_create_education(self):
        edu = Education.objects.create(
            course="BSI", institution="UF", period="2020-2024"
        )
        self.assertEqual(str(edu), "BSI")


class CourseModelTest(TestCase):
    def test_create_course(self):
        c = Course.objects.create(name="Django Course", platform="Udemy")
        self.assertEqual(str(c), "Django Course")


class ContactModelTest(TestCase):
    def test_create_contact(self):
        c = Contact.objects.create(email="test@test.com")
        self.assertEqual(str(c), "Contato")


class PostModelTest(TestCase):
    def setUp(self):
        self.tag = PostTag.objects.create(name="Python")
        self.post = Post.objects.create(
            title="Post title",
            content="Content here",
            published=True,
        )
        self.post.tags.add(self.tag)

    def test_post_creation(self):
        self.assertEqual(str(self.post), "Post title")
        self.assertTrue(self.post.slug)

    def test_post_tags(self):
        self.assertIn(self.tag, self.post.tags.all())


class PostTagModelTest(TestCase):
    def test_create_tag(self):
        tag = PostTag.objects.create(name="Django")
        self.assertEqual(str(tag), "Django")


class MessageModelTest(TestCase):
    def test_create_message(self):
        msg = Message.objects.create(
            name="John", email="john@test.com", body="Hello"
        )
        self.assertIn(str(msg), ["John - (sem assunto)", "John - "])
        self.assertFalse(msg.read)


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        Technology.objects.create(name="Python")
        Project.objects.create(title="P1", description="Desc")

    def test_home_status(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_context(self):
        response = self.client.get(reverse("home"))
        self.assertIn("projects", response.context)
        self.assertIn("technologies", response.context)

    def test_home_search(self):
        response = self.client.get(reverse("home") + "?q=P1")
        self.assertEqual(response.status_code, 200)


class ProjectDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(
            title="Test", description="Desc", slug="test"
        )

    def test_detail_status(self):
        response = self.client.get(
            reverse("project_detail", kwargs={"slug": "test"})
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_404(self):
        response = self.client.get(
            reverse("project_detail", kwargs={"slug": "nonexistent"})
        )
        self.assertEqual(response.status_code, 404)


class ProjectCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser("admin", "a@a.com", "pass")
        self.project = Project.objects.create(
            title="P1", description="Desc", slug="p1"
        )

    def test_create_view_redirects_when_not_logged_in(self):
        response = self.client.get(reverse("project_create"))
        self.assertNotEqual(response.status_code, 200)

    def test_create_view_when_logged_in(self):
        self.client.login(username="admin", password="pass")
        response = self.client.get(reverse("project_create"))
        self.assertEqual(response.status_code, 200)

    def test_update_view_when_logged_in(self):
        self.client.login(username="admin", password="pass")
        response = self.client.get(
            reverse("project_update", kwargs={"slug": "p1"})
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_view_when_logged_in(self):
        self.client.login(username="admin", password="pass")
        response = self.client.get(
            reverse("project_delete", kwargs={"slug": "p1"})
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        self.client.login(username="admin", password="pass")
        response = self.client.post(
            reverse("project_delete", kwargs={"slug": "p1"})
        )
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(Project.objects.count(), 0)


class BlogViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        Post.objects.create(
            title="Post 1", content="Content", published=True, slug="post-1"
        )

    def test_blog_list(self):
        response = self.client.get(reverse("blog_list"))
        self.assertEqual(response.status_code, 200)

    def test_blog_detail(self):
        response = self.client.get(
            reverse("blog_detail", kwargs={"slug": "post-1"})
        )
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_404(self):
        response = self.client.get(
            reverse("blog_detail", kwargs={"slug": "nonexistent"})
        )
        self.assertEqual(response.status_code, 404)


class ContactFormTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_form_submission(self):
        data = {
            "contact": "1",
            "name": "John",
            "email": "john@test.com",
            "subject": "Hello",
            "body": "Test message",
        }
        response = self.client.post(reverse("home"), data)
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(Message.objects.count(), 1)


class SitemapTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sitemap(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)


class RobotsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_robots_txt(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sitemap", response.content)

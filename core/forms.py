from django import forms
from .models import Project, Message, Post


class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["name", "email", "subject", "body"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Seu nome", "required": True}),
            "email": forms.EmailInput(attrs={"placeholder": "seu@email.com", "required": True}),
            "subject": forms.TextInput(attrs={"placeholder": "Assunto (opcional)"}),
            "body": forms.Textarea(attrs={"placeholder": "Sua mensagem...", "rows": 5, "required": True}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title", "description", "full_description",
            "image", "gif", "github_link", "deploy_link",
            "technologies", "order",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "full_description": forms.Textarea(attrs={"rows": 6}),
            "technologies": forms.CheckboxSelectMultiple,
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "summary", "image", "tags", "published"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 10}),
            "summary": forms.Textarea(attrs={"rows": 3}),
        }

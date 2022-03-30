from django import forms

from .models import Project


class NewProjectForm(forms.ModelForm):

    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'text',
                "placeholder": "Tag",
            }
        )
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                "rows": 3,
                "aria-label": ".form-control-sm",
                "placeholder": "Description (optional)",
            })
    )

    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'author'
        )

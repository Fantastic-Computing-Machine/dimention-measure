from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import ModelForm

from .models import Inspection, Defect


class NewInspectionForm(ModelForm):
    name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "text",
                "placeholder": "Name",
            }
        )
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "aria-label": ".form-control-sm",
                "placeholder": "Description (optional)",
            }
        )
    )

    class Meta:
        model = Inspection
        fields = (
            "name",
            "description",
            "inspector",
        )


# class NewDefectForm(ModelForm):

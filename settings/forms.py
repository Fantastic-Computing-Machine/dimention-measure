from settings.models import TermsHeading
from django import forms
from ckeditor.widgets import CKEditorWidget


class TermsAndConditionForm(forms.ModelForm):

    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control",
                "type": "text",
                "placeholder": "Heading",

            }
        )
    )
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = TermsHeading
        fields = (
            "name",
            "organization",
            "content",
        )

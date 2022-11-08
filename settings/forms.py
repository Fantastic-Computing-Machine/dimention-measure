from authentication.models import Organization
from settings.models import OrganizationTNC
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
    content = forms.CharField(
        required=True,
        widget=CKEditorWidget(
            attrs={
                "class": "form-control",
            }
        )
    )

    organization = forms.ModelChoiceField(
        required=False,
        queryset=Organization.objects.all(),
        label=False,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "aria-label": ".form-control",
                "placeholder": "Unit",
                "type": "button",
                "readonly": True,
                "hidden": True,
            }
        )
    )

    class Meta:
        model = OrganizationTNC
        fields = (
            "name",
            "organization",
            "content",
        )

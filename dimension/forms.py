from django import forms

from .models import Project, Dimension


class BasicFormsFields(forms.ModelForm):
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
        ),
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 2,
                "aria-label": ".form-control-sm",
                "placeholder": "Description (optional)",
            }
        ),
    )


class NewProjectForm(BasicFormsFields):
    name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "text",
                "placeholder": "Project name should be unique",
            }
        ),
    )

    class Meta:
        model = Project
        fields = ("name", "description", "author")


class UpdateProjectForm(BasicFormsFields):
    name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "text",
                "placeholder": "Name (unique)",
            }
        ),
    )

    class Meta:
        model = Project
        fields = ("name", "description")


class NewDimensionForm(BasicFormsFields):
    length_feet = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "number",
                "placeholder": "Width (in feet)",
                "step": ".01",
            }
        ),
    )

    length_inches = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "number",
                "placeholder": "Width (in inches)",
                "step": ".01",
            }
        ),
    )

    width_feet = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "number",
                "placeholder": "Height (in feet)",
                "step": ".01",
            }
        ),
    )

    width_inches = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "number",
                "placeholder": "Height (in inches)",
                "step": ".01",
            }
        ),
    )

    rate = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "number",
                "placeholder": "Rate",
                "step": ".01",
                "value": "0.0",
            }
        ),
    )

    class Meta:
        model = Dimension
        fields = (
            "project",
            "name",
            "description",
            "length_feet",
            "length_inches",
            "width_feet",
            "width_inches",
            "rate",
            "sqm",
            "sqft",
        )


class UpdateDimensionForm(NewDimensionForm):
    sqm = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "text",
                "placeholder": "Sqm",
                "disabled": "true",
                "readonly": "true",
            }
        ),
    )
    sqft = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "text",
                "placeholder": "Sqft",
                "disabled": "true",
                "readonly": "true",
            }
        ),
    )

    class Meta:
        model = Dimension
        fields = (
            "name",
            "description",
            "length_feet",
            "length_inches",
            "width_feet",
            "width_inches",
            "rate",
            "sqm",
            "sqft",
        )

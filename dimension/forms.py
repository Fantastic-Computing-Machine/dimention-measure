from django import forms

from .models import Project, Dimension


class NewProjectForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', "rows": 3, })
    )

    class Meta:
        model = Project
        fields = ('name', 'description', 'author')


class NewDimensionForm(forms.ModelForm):
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
    length = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'number',
                "placeholder": "Lenght (in meters)",
                "step": ".01",
                "oninput": "areas()",
            }
        )
    )
    width = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'number',
                "placeholder": "Width (in meters)",
                "step": ".01",
                "oninput": "areas()",
            }
        )
    )
    rate = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'number',
                "placeholder": "Rate",
                "step": ".01",
                "oninput": "areas()",
            }
        )
    )

    class Meta:
        model = Dimension
        fields = ('project', 'name', 'description', 'length', 'width', 'rate')


class UpdateDimensionForm(forms.ModelForm):
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
    length = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'number',
                "placeholder": "Lenght (in meters)",
                "step": ".01",
                "oninput": "areas()",
            }
        )
    )
    width = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'number',
                "placeholder": "Width (in meters)",
                "step": ".01",
                "oninput": "areas()",
            }
        )
    )
    rate = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'number',
                "placeholder": "Rate",
                "step": ".01",
                "oninput": "areas()",
            }
        )
    )

    class Meta:
        model = Dimension
        fields = ('name', 'description', 'length', 'width', 'rate')

class DeleteProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('is_deleted',)


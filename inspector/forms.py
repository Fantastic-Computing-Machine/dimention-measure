from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import ModelForm

from .models import Inspection, Defect

from dimension.forms import BasicFormsFields


class NewInspectionForm(BasicFormsFields):

    class Meta:
        model = Inspection
        fields = (
            "name",
            "description",
            "inspector",
        )


# class NewDefectForm(ModelForm):

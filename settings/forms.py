from settings.models import TermsHeading, TermsContent
from django import forms


# class TermsHeadingForm(forms.ModelForm):

#     name = forms.CharField(
#         max_length=200,
#         required=True,
#         widget=forms.TextInput(
#             attrs={
#                 "class": "form-control",
#                 "aria-label": ".form-control-sm",
#                 "type": "text",
#                 "placeholder": "Section Name",
#                 "readonly": True,

#             }
#         )
#     )

#     class Meta:
#         model = TermsHeading
#         fields = (
#             "name",
#             "organization",
#         )

from django import forms
from django.conf import settings

from client_and_company.models import Client


class NewClientForm(forms.ModelForm):

    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'text',
                "placeholder": "Name",
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
            }
        )
    )

    phoneNumber = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'tel',
                "placeholder": "Phone Number (optional)",
                "maxlength": "11",
            }
        )
    )

    address_1 = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'text',
                "placeholder": "Address 1",
            }
        )
    )

    address_2 = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'text',
                "placeholder": "Address 2 (optional)",
            }
        )
    )

    landmark = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'text',
                "placeholder": "Landmark (optional)",
            }
        )
    )

    town_city = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'text',
                "placeholder": "Town/City",
            }
        )
    )

    zip_code = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'number',
                "placeholder": "Zip code",
                "maxlength": "7",
            }
        )
    )

    state = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.Select(
            choices=settings.STATE_CHOICES,
            attrs={
                "class": "form-select",
                "aria-label": ".form-control-sm",
                "placeholder": "State"
            }
        )
    )

    class Meta:
        model = Client
        fields = {
            'name',
            'phoneNumber',
            'description',
            'address_1',
            'address_2',
            'landmark',
            'town_city',
            'zip_code',
            'state',
            'organization',
            'created_by',
        }

class UpdateClientForm(forms.ModelForm):

    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'text',
                "placeholder": "Name",
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
            }
        )
    )

    phoneNumber = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'tel',
                "placeholder": "Phone Number (optional)",
                "maxlength": "11",
            }
        )
    )

    address_1 = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'text',
                "placeholder": "Address 1",
            }
        )
    )

    address_2 = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'text',
                "placeholder": "Address 2 (optional)",
            }
        )
    )

    landmark = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'text',
                "placeholder": "Landmark (optional)",
            }
        )
    )

    town_city = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'text',
                "placeholder": "Town/City",
            }
        )
    )

    zip_code = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'number',
                "placeholder": "Zip code",
                "maxlength": "7",
            }
        )
    )

    state = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.Select(
            choices=settings.STATE_CHOICES,
            attrs={
                "class": "form-select",
                "aria-label": ".form-control-sm",
                "placeholder": "State"
            }
        )
    )

    class Meta:
        model = Client
        fields = {
            'name',
            'phoneNumber',
            'description',
            'address_1',
            'address_2',
            'landmark',
            'town_city',
            'zip_code',
            'state',
            
        }

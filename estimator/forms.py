from django import forms

from .models import *


class NewProjectForm(forms.ModelForm):

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

    client = forms.ModelChoiceField(
        required=True,
        queryset=Client.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "aria-label": ".form-control-sm",
                "placeholder": "Client",
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

    class Meta:
        model = Project
        fields = (
            'name',
            'client',
            'description',
            'author'
        )


class NewEstimateItemForm(forms.ModelForm):
    room = forms.ModelChoiceField(
        required=True,
        queryset=Room.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "aria-label": ".form-control-sm",
                "placeholder": "Room",
            }
        )
    )
    room_item = forms.ModelChoiceField(
        required=True,
        queryset=RoomItem.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "aria-label": ".form-control-sm",
                "placeholder": "Room Item",
            }
        )
    )
    room_item_description = forms.ModelChoiceField(
        required=True,
        queryset=RoomItemDescription.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "aria-label": ".form-control-sm",
                "placeholder": "Item Description",
            }
        )
    )

    quantity = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "aria-label": ".form-control-sm",
                "type": 'number',
                "placeholder": "Amount",
                "step": ".01",
            }
        )
    )

    class Meta:
        model = Estimate
        fields = (
            'project',
            'room',
            'room_item',
            'room_item_description',
            'quantity',
        )


class NewRoomForm(forms.ModelForm):
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

    class Meta:
        model = Room
        fields = (
            'name',
        )


class NewRoomItemForm(forms.ModelForm):
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

    class Meta:
        model = RoomItem
        fields = (
            'name',
        )


class NewClient(forms.ModelForm):

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
            }
        )
    )

    class Meta:
        model = Client
        fields = {
            'name',
            'phoneNumber',
            'description',

        }

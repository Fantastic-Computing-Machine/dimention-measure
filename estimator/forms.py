from faulthandler import disable
from typing_extensions import Required
from django import forms

from .models import Estimate, Project, Room, RoomItem, RoomItemDescription
from client_and_company.models import Client
from settings.models import Unit


class NewProjectForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
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
                "class": "form-control",
                "rows": 3,
                "aria-label": ".form-control-sm",
                "placeholder": "Description (optional)",
            }
        )
    )

    class Meta:
        model = Project
        fields = (
            "name",
            "client",
            "description",
            "author"
        )


class UpdateProjectForm(forms.ModelForm):

    name = forms.CharField(
        max_length=200,
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
                "class": "form-control",
                "rows": 3,
                "aria-label": ".form-control-sm",
                "placeholder": "Description (optional)",
            }
        )
    )

    class Meta:
        model = Project
        fields = (
            "name",
            "client",
            "description",
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

    length = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "number",
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
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "number",
                "placeholder": "Width (in meters)",
                "step": ".01",
                "oninput": "areas()",
            }
        )
    )

    discount = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "number",
                "placeholder": "Discount percentage",
                "step": ".01",
            }
        )
    )

    quantity = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "number",
                "placeholder": "Quantity",
                "step": ".01",
                "id": "forQuantity",
                "disabled": "disabled"
            }
        )
    )

    class Meta:
        model = Estimate
        fields = (
            "project",
            "room",
            "room_item",
            "room_item_description",
            "quantity",
            "length",
            "width",
            "discount",

        )


class NewRoomForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
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

    class Meta:
        model = Room
        fields = (
            "name",
        )


class NewRoomItemForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
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

    class Meta:
        model = RoomItem
        fields = (
            "name",
        )


class NewRoomItemDescriptionForm(forms.ModelForm):
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "aria-label": ".form-control-sm",
                "placeholder": "Description",
            }
        )
    )

    rate = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "number",
                "placeholder": "Rate",
                "step": ".01",
            }
        )
    )

    unit = forms.ModelChoiceField(
        required=True,
        queryset=Unit.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "aria-label": ".form-control-sm",
                "placeholder": "Unit",
            }
        )
    )

    class Meta:
        model = RoomItemDescription
        fields = (
            "description",
            "unit",
            "rate"
        )


class DiscountForm(forms.ModelForm):

    discount = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "number",
                "placeholder": "Discount",
                "step": ".01",
            }
        )
    )

    class Meta:
        model = Project
        fields = (
            "discount",
        )

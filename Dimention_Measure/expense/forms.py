from django import forms

from .models import Payee, Expense, PAYMENT_STATUS


class NewPayeeForm(forms.ModelForm):
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
        model = Payee
        fields = ('name', 'description', 'phoneNumber')


class UpdatePayeeForm(forms.ModelForm):
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
        model = Payee
        fields = ('name', 'description', 'phoneNumber')


class CreateExpenseForm(forms.ModelForm):

    payee = forms.ModelChoiceField(
        required=True,
        queryset=Payee.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "aria-label": ".form-control-sm",
                "placeholder": "Payee",
            }
        )
    )

    amount = forms.CharField(
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

    payment_status = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.Select(
            choices=PAYMENT_STATUS,
            attrs={
                "class": "form-select",
                "aria-label": ".form-control-sm",
                "placeholder": "Payment-satus"
            }
        )
    )

    class Meta:
        model = Expense
        fields = (
            'project',
            'payee',
            'amount',
            'payment_status'
        )


class UpdateExpenseForm(forms.ModelForm):

    amount = forms.CharField(
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

    payment_status = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.Select(
            choices=PAYMENT_STATUS,
            attrs={
                "class": "form-select",
                "aria-label": ".form-control-sm",
                "placeholder": "Payment-satus"
            }
        )
    )

    class Meta:
        model = Expense
        fields = (
            'project',
            'payee',
            'amount',
            'payment_status'
        )
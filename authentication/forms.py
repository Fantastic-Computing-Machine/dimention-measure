from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from authentication.models import CompanyUser, Organization
from django.conf import settings


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = CompanyUser
        fields = ("username", "email", "first_name",
                  "last_name", "organization", "access_level")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin"s
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see this user's password, but you can change the password using <a style='olor: red ' href=\"../password/\">this form</a>."))

    class Meta:
        model = CompanyUser
        fields = ("username", "password", "date_of_birth",
                  "is_active", "is_admin")


class OrganizationForm(forms.ModelForm):
    company_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "text",
                "placeholder": "Company Name",

            }
        )
    )
    manager_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "text",
                "placeholder": "Manager name",

            }
        )
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "email",
                "placeholder": "Email",
            }
        )
    )

    phoneNumber = forms.CharField(
        max_length=10,
        required=True,
        validators=[RegexValidator(r"\d{10}$")],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "tel",
                "placeholder": "Phone Number (optional)",
            }
        )
    )

    website = forms.URLField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "url",
                "placeholder": "Website (optional)",
            }
        )
    )

    gstn = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "text",
                "placeholder": "GSTN",
            }
        )
    )

    address_1 = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "text",
                "placeholder": "Address 1",
            }
        )
    )

    address_2 = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "text",
                "placeholder": "Address 2 (optional)",
            }
        )
    )

    landmark = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "text",
                "placeholder": "Landmark (optional)",
            }
        )
    )

    town_city = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "text",
                "placeholder": "Town/City",
            }
        )
    )

    zip_code = forms.CharField(
        max_length=7,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "type": "number",
                "placeholder": "Zip code",
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

    bank_account_holder_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "placeholder": "Bank Account Holder Name",
            }
        )
    )

    bank_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "placeholder": "Bank Name",
            }
        )
    )

    bank_account_number = forms.CharField(
        max_length=18,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "placeholder": "Bank Account Number",
            }
        )
    )

    bank_branch = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "placeholder": "Bank Branch",
            }
        )
    )

    bank_ifsc_code = forms.CharField(
        max_length=11,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "aria-label": ".form-control-sm",
                "placeholder": "Bank IFSC Code",
            }
        )
    )

    class Meta:
        model = Organization
        fields = [
            # PII
            "company_name",
            "manager_name",
            "phoneNumber",
            "email",
            "website",
            "gstn",
            # Reach
            "address_1",
            "address_2",
            "landmark",
            "town_city",
            "zip_code",
            "state",
            # Banking
            "bank_account_holder_name",
            "bank_name",
            "bank_account_number",
            "bank_branch",
            "bank_ifsc_code",
        ]

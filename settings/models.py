from ckeditor.fields import RichTextField
from django.urls import reverse
from django.db import models


from authentication.models import Organization


class Unit(models.Model):
    unit = models.CharField(max_length=255)

    def __str__(self):
        return str(self.unit)


class TermsHeading(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE)
    content = RichTextField(null=False)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("terms_and_conditions")


# class TermsContent(models.Model):
#     heading = models.ForeignKey(TermsHeading, on_delete=models.CASCADE)
#     description = models.TextField(
#         blank=True, null=True)

#     def __str__(self):
#         return str(self.heading.name) + ' | ' + str(self.description[:30])

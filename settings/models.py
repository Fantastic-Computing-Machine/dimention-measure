from django.db import models

from django_quill.fields import QuillField

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

    def __str__(self):
        return str(self.name)


class TermsContent(models.Model):
    heading = models.ForeignKey(TermsHeading, on_delete=models.CASCADE)
    description = models.TextField(
        blank=True, null=True)
    content = QuillField(blank=True)

    def __str__(self):
        return str(self.heading.name) + ' | ' + str(self.description[:30])

from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


User = user_model()

DEFECT_STATUS = [
    ("C", "Completed"),
    ("O", "Overdue"),
    ("P", "Pending"),
    ("U", "Upcoming"),
    ("A", "Active"),
    ("X", "Cancelled"),
    ("N", "Not Started"),
]


class Inspection(models.Model):
    name = models.CharField(max_length=255, unique=True,
                            help_text="Name of the inspector project")
    inspector = models.ForeignKey(User, on_delete=models.CASCADE,
                                  help_text="User who created the inspector project")
    description = models.TextField(
        max_length=255, blank=True, null=True, help_text="Description of the inspector project")
    created_on = models.DateTimeField(
        auto_now_add=True, help_text="Date and time when the inspector project was created")
    is_deleted = models.BooleanField(
        default=False, help_text="Is the inspector project deleted?")
    deleted_on = models.DateTimeField(
        blank=True, null=True, help_text="Date and time when the inspector project was deleted")

    def __str__(self):
        return str(self.name)

    def save(self):
        self.name = self.name.strip().replace(" ", "-")
        if self.is_deleted:
            self.deleted_on = datetime.datetime.now()
        return super(Inspection, self).save()

    def save_model(self, request, obj, form, change):
        obj.inspector = request.user.id
        super().save_model(request, obj, form, change)


class Defect(models.Model):
    title = models.CharField(max_length=255, unique=True,
                             help_text="Title of the defect")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="User who created the defect")
    project = models.ForeignKey(
        Inspection, on_delete=models.CASCADE, help_text="Project where the defect was found")
    body = models.TextField(max_length=255, blank=False,
                            null=False, help_text="Description of the defect")
    status = models.CharField(max_length=1,
                              choices=DEFECT_STATUS,
                              default="P",)
    created_on = models.DateTimeField(
        auto_now_add=True, help_text="Date and time when the defect was created")
    images = models.ImageField(
        null=True,
        blank=True,
        upload_to="inspector/defect/",
        help_text="Image of the defect(s)",
    )
    due_date = models.DateField(
        blank=True, null=True, help_text="Date when the defect should be Fixed!")

    is_deleted = models.BooleanField(
        default=False, help_text="Is the defect removed?")

    deleted_on = models.DateTimeField(
        blank=True, null=True, help_text="Date and time when the inspector project was deleted")

    def __str__(self):
        return str(self.title) + " | " + str(self.status)

    def save(self):
        self.title = self.title.strip().replace(" ", "-")
        if self.is_deleted:
            self.deleted_on = datetime.datetime.now()
        return super(Defect, self).save()

    def get_absolute_url(self):
        return reverse("home")

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta


class TodoTeam(models.Model):
    name = models.CharField("My Group", max_length=50)
    description = models.CharField(
        "Enter a Description for your team!", max_length=255, blank=False)
    # ManyToMany fields by default prevent dupes. Logic on frontend might still need to be made to support this. idk
    users = models.ManyToManyField('TodoUser', blank=True)

    def __str__(self):
        return self.name


class TodoUser(AbstractUser):
    email = models.EmailField(unique=True)
    users = models.ManyToManyField(TodoTeam, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class TodoItem(models.Model):
    LEVEL_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             blank=True, on_delete=models.CASCADE)  # For personal todo items
    team = models.ForeignKey(
        TodoTeam, null=True, blank=True, on_delete=models.CASCADE)  # For team
    # CASCADE means that when the user/group is deleted, so too is the item

    title = models.CharField(max_length=50, null=True,
                             blank=True, default="My Task")
    description = models.TextField(
        max_length=500, null=True, blank=True, default='')
    # MOVED COMPLETED
    due_date = models.DateTimeField(default=datetime.datetime.now)
    priority = models.CharField(
        max_length=10, choices=LEVEL_CHOICES, default='M')

    # =============
    # New Fields
    # =============
    # May need tweaking depending on how we want to do "No Category Items"
    category = models.CharField(null=True, blank=False, max_length=30)
    completed = models.FloatField(  # Completed is now a Float instead of a boolean, should only allow archival if >=100.0
        default=0.00,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(100.0),
        ],
        null=False,
        blank=False,
    )

    assignee = models.ForeignKey('TodoUser', null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name='assigned_user')  # ForeignKey to TodoUser

    # Reminder Feature
    reminder_date = models.DateTimeField(
        default=datetime.datetime.now)  # Time To be reminded at

    # Timer Feature
    total_duration = models.DurationField(default=timedelta(
        0), null=False, blank=False)  # Track total time across stops/starts
    current_start_time = models.DateTimeField(null=True, blank=True)

    def start_timer(self):  # Calling this fn starts the timer.
        if self.current_start_time is None:  # Start the timer only if it's not already running
            self.current_start_time = timezone.now()
            self.save()
        else:
            raise Exception("Timer is already running!")

    def stop_timer(self):  # Calling this fn stops the timer.
        if self.current_start_time is not None:  # Stop the timer only if it's running
            elapsed_time = timezone.now() - self.current_start_time
            self.total_duration += elapsed_time  # Add time to total duration
            self.current_start_time = None  # Reset current start time
            self.save()
        else:
            raise Exception("Timer is not running!")

    # Reset Timer, NOT a required feature, but I have this for debugging reasons, or if we want to add it later.
    def reset_timer(self):
        if self.current_start_time is None:
            self.total_duration = timedelta(0)
            self.save()
        else:
            raise Exception("Timer is running! Stop it first!")

    def save(self, *args, **kwargs):
        # Automatically set assignee based on ownership
        if self.user:
            self.assignee = self.user  # MAKE SURE THE FORMS DO NOT ALLOW YOU TO CHANGE THIS
        elif self.team:
            if self.team.users.exists():
                self.assignee = self.team.users.first()  # By Defult
            else:
                raise ValidationError("No Members in Team! How??")

        super().save(*args, **kwargs)  # Save

    def clean(self):
        # Ensure that either user or team is filled, but not both
        if self.user and self.team:
            raise ValidationError(
                "A TodoItem can belong to either a user or a team, but not both.")
        if not self.user and not self.team:
            raise ValidationError(
                "A TodoItem must belong to either a user or a team.")

        if self.reminder_date < timezone.now():
            raise ValidationError("Reminder time cannot be in the past.")

        if self.reminder_date > self.due_date:
            raise ValidationError(
                "Reminder time cannot be after the due date.")

    def __str__(self):
        return self.title

    class Meta:
        ordering=['due_date']

class TeamInvite(models.Model):
    team = models.ForeignKey(TodoTeam, on_delete=models.CASCADE)
    invited_user = models.ForeignKey(TodoUser, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
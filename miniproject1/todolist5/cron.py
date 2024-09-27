from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from .models import TodoItem

FORGIVENESS_WINDOW = timedelta(seconds=10)



def remind_users():
    print("REMINDER CRON TASK RUNNING" + timezone.now())
    now = timezone.now()
    todo_items = TodoItem.objects.filter(reminder_date__range=(now - FORGIVENESS_WINDOW, now + FORGIVENESS_WINDOW))
    for item in todo_items:
        if item.assignee and item.assignee.email:
            send_mail(
                'Impending Deadline',
                f'you have and impending deadline for {item.title}!',
                "{csc394.group5@gmail.com}",
                [item.assignee.email],
                fail_silently=False,
            )
            print(f"REMINDER EMAIL DELIVERED TO {item.assignee.email} FOR TASK f{item.title}" )
    
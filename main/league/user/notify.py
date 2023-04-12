from django.utils import timezone

from ...models import Notification


def notify(user, message):
    notification = Notification(user=user, message=message, date=timezone.now())
    notification.save()

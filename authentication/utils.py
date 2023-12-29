from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth import get_user_model as user_model

User = user_model()


def get_active_logged_in_users():
    """Method to get all active logged in users"""
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())

    user_ids = [
        int(session.get_decoded().get("_auth_user_id")) for session in active_sessions
    ]

    active_users = User.objects.filter(id__in=user_ids)
    return active_users

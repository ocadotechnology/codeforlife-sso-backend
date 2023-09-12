# Generated by Django 2.0 on 2020-10-28 17:36

import datetime
from uuid import uuid4

from django.db import migrations
from django.utils import timezone


def verify_portaladmin(apps, schema_editor):
    """
    This migration is so that we can still log in using the portaladmin User, as the
    login form now requires email verification.
    """
    User = apps.get_model("auth", "User")
    EmailVerification = apps.get_model("common", "EmailVerification")

    portaladmin = User.objects.get(username="portaladmin")

    EmailVerification.objects.create(
        user=portaladmin,
        email=portaladmin.email,
        token=uuid4().hex[:30],
        expiry=timezone.now() + datetime.timedelta(hours=1),
        verified=True,
    )


def revert_portaladmin_verification(apps, schema_editor):
    User = apps.get_model("auth", "User")
    EmailVerification = apps.get_model("common", "EmailVerification")

    portaladmin = User.objects.get(username="portaladmin")
    portaladmin_verification = EmailVerification.objects.get(user=portaladmin)
    portaladmin_verification.delete()


class Migration(migrations.Migration):

    dependencies = [("portal", "0061_make_portaladmin_teacher")]

    operations = [
        migrations.RunPython(verify_portaladmin, revert_portaladmin_verification)
    ]

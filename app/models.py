from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth import get_user_model as user_model


class User(AbstractUser):

    account_id = models.IntegerField(null=True, db_index=True)
    access_token = models.CharField(max_length=32, null=True)


class UserAssociation(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        verbose_name=_("user"),
        related_name='user',
        on_delete='CASCASE'
    )
    site_user_id = models.IntegerField()
    site_url = models.CharField(max_length=100)
    site_name = models.CharField(max_length=50)

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    account_id = models.IntegerField(null=True, db_index=True)
    access_token = models.CharField(max_length=32, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


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
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Tags(models.Model):

    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Question(models.Model):

    user_profile = models.ForeignKey(
        UserAssociation,
        null=False,
        verbose_name=_("user_profile"),
        related_name='user_assocciaiton',
        on_delete='CASCASE'
    )
    site_question_id = models.IntegerField(unique=True)
    site_question_url = models.CharField(max_length=500)
    tags = models.ManyToManyField(Tags)
    content = models.TextField()
    asked_on = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Balance(models.Model):

    amount = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    user = models.OneToOneField(User, on_delete='CASCADE')
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()


class Transactions(models.Model):
    STATE_CHOICES = ('INITIATED', 'SUCCESSFUL', 'FAILED')

    transaction_id = models.CharField(null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    state = models.CharField(choices=STATE_CHOICES)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()


class UserActivity(models.Model):
    ACTION_CHOICES = (
        'TOP UP',
        'FUNDED BOUNTY',
        'CLAIMED BOUNTY',
        'WITHDRAW MONEY',
        'CANCEL BOUNTY',
    )

    user = models.OneToOneField(User, on_delete='CASCADE')
    action = models.CharField(max_length=32, choices=ACTION_CHOICES)
    transaction = models.OneToOneField(Transactions, null=True, on_delete='CASCADE')


class Bounty(models.Model):
    STATE_CHOICES = ('OPEN', 'COMPLETED', 'CANCELLED', 'EXPIRED')

    question = models.OneToOneField(Question, on_delete='CASCADE')
    claimed_user = models.OneToOneField(UserAssociation, null=True, on_delete='CASCADE')
    amount = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    state = models.CharField(max_length=32, choices=STATE_CHOICES)
    expiry_date = models.DateTimeField()
    completed_at = models.DateTimeField(null=True)
    cancelled_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()


class Claim(models.Model):

    bounty = models.ManyToManyField(Bounty)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()

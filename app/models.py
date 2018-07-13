from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    account_id = models.IntegerField(null=True, db_index=True)
    access_token = models.CharField(max_length=32, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StackExchangeSite(models.Model):

    name = models.CharField(max_length=50)
    site_url = models.CharField(max_length=100)
    api_site_parameter = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
    site = models.ForeignKey(StackExchangeSite, on_delete='CASCADE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):

    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    bountied_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        verbose_name=_("user"),
        related_name='bountied_user',
        on_delete='CASCASE'
    )
    site_question_id = models.IntegerField(unique=True)
    site_question_url = models.CharField(max_length=500)
    site = models.ForeignKey(StackExchangeSite, on_delete='CASCADE')
    tags = models.ManyToManyField(Tag)
    title = models.TextField()
    asked_on = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Balance(models.Model):

    amount = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    user = models.ForeignKey(User, on_delete='CASCADE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    STATE_CHOICES = (
        ('INITIATED', 'EXPIRED'),
        ('SUCCESSFUL', 'SUCCESSFUL'),
        ('FAILED', 'FAILED')
    )

    transaction_id = models.CharField(max_length=50, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    state = models.CharField(max_length=32, choices=STATE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserActivity(models.Model):
    ACTION_CHOICES = (
        ('TOP UP', 'TOP UP'),
        ('FUNDED BOUNTY', 'FUNDED BOUNTY'),
        ('CLAIMED BOUNTY', 'CLAIMED BOUNTY'),
        ('WITHDRAW MONEY', 'WITHDRAW MONEY'),
        ('CANCEL BOUNTY', 'CANCEL BOUNTY'),
    )

    user = models.ForeignKey(User, on_delete='CASCADE')
    action = models.CharField(max_length=32, choices=ACTION_CHOICES)
    transaction = models.ForeignKey(Transaction, null=True, on_delete='CASCADE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Bounty(models.Model):
    STATE_CHOICES = (
        ('OPEN', 'OPEN'),
        ('COMPLETED', 'COMPLETED'),
        ('CANCELLED', 'CANCELLED'),
        ('EXPIRED', 'EXPIRED')
    )

    question = models.ForeignKey(Question, on_delete='CASCADE')
    claimed_user = models.ForeignKey(UserAssociation, null=True, on_delete='CASCADE')
    amount = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    state = models.CharField(max_length=32, choices=STATE_CHOICES)
    expiry_date = models.DateTimeField()
    completed_at = models.DateTimeField(null=True)
    cancelled_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Claim(models.Model):

    bounty = models.ManyToManyField(Bounty)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

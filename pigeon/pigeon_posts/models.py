from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
from django.conf import settings
from django.utils.text import slugify
from django.db import models

from account.models import Account


class Post(models.Model):
    date_published = models.DateTimeField(
        auto_now_add=True, verbose_name="Published Date")
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="Last Updated")
    body = models.TextField(max_length=240, null=False, blank=False,
                            help_text="Write a post in 240 characters or less")
    author = models.ForeignKey(Account, on_delete=models.CASCADE, null=False,
                               default=1, blank=False, verbose_name="Author", related_name="Author")

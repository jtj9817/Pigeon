from django.db import models
from account.models import Account
# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, null=False,
                               blank=False, verbose_name="Sender", related_name='sender')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, null=False,
                                 blank=False, verbose_name="Receiver", related_name='receiver')
    content = models.TextField(max_length=512, blank=False, null=False,
                               unique=False, editable=False, verbose_name="Message")
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone


# Create your models here.
class Message(models.Model):
    ORDINARY = 'ordinary'
    URGENT = 'urgent'
    MESSAGE_LEVEL_CHOICES = [
        (ORDINARY, 'Ordinary'),
        (URGENT, 'Urgent'),
    ]

    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    level = models.CharField(max_length=10, choices=MESSAGE_LEVEL_CHOICES, default=ORDINARY)
    title = models.CharField(max_length=255)
    content = models.TextField()
    sent_time = models.DateTimeField(default=timezone.now)

    # 系统消息由administrator发出reciever可以设置为三个组teacher，student，administrator表示所有人，系统消息的优先级一般为Urgent
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-sent_time']

    
class MessageRead(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
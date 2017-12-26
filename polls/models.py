import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    labeled = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return self.question_text

class Conversation(models.Model):
    question = models.ForeignKey(Question)
    roundid = models.IntegerField()
    speaker = models.CharField(max_length=200)
    center_bool = models.IntegerField(default=0)
    Conversation_txt = models.CharField(max_length=200)

    def __str__(self):
        return self.Conversation_txt

    class Meta:
        ordering = ['roundid']


class Label(models.Model):
    question = models.ForeignKey(Question)
    roundid = models.IntegerField()
    center_bool = models.IntegerField(default=0)
    label_text = models.CharField(max_length=200)
    def __str__(self):
        return self.label_text

    class Meta:
        unique_together = (('question', 'roundid'),)

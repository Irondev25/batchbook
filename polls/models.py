from django.db import models
from django.shortcuts import reverse

from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Poll(models.Model):
    question = models.CharField(max_length=256)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'poll'
        verbose_name_plural = 'polls'
        ordering = ('pub_date',)
    
    def __str__(self):
        return self.question
    
    def get_absolute_url(self):
        return reverse('poll:poll_detail', kwargs={'pk':self.pk})


class Choice(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=100)
    vote = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.choice_text
    
    def upvote(self):
        self.vote += 1
        self.save()
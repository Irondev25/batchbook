from django.contrib.auth import get_user_model
from django.db import models
from django.forms.fields import CharField, DateTimeField

from .utils import smart_truncate


USER = get_user_model()

# Create your models here.
class QuestionModel(models.Model):
    que_title = models.CharField("Question Title", max_length=60)
    que_text = models.TextField("Question")
    author = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="questions")
    pub_date = models.DateTimeField(auto_now_add=True)
    save_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"
        ordering = ['-pub_date', 'que_text']

    
    def __str__(self):
            return smart_truncate(self.que_text, 30) + " on "+ self.pub_date
    

class AnswerModel(models.Model):
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name="answers")
    ans_text = models.TextField()
    author = models.CharField(default="Anonymous", max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    save_date= models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
            return smart_truncate(self.ans_text, 50) + " by" + self.author




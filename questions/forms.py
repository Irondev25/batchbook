from django import forms

from .models import QuestionModel, AnswerModel

class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionModel
        fields = ('que_text',)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = AnswerModel
        fields = ('ans_text',)

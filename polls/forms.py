from django import forms

from .models import Poll, Choice



class PollForm(forms.ModelForm):

    class Meta:
        model = Poll
        fields = ('question',)
        widgets = {
            'question': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'author': forms.HiddenInput()
        }


class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ('choice_text','question')
        widgets = {
            'choice_text': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'question': forms.HiddenInput()
        }
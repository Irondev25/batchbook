from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import QuestionModel, AnswerModel
from .forms import QuestionForm, AnswerForm
# Create your views here.


class QuestionList(ListView):
    context_object_name = 'question_list'
    model = QuestionModel
    paginate_by = 5
    template_name = 'questions/question_list.html'

class QuestionDetail(DetailView):
    context_object_name = 'question'
    model = QuestionModel
    
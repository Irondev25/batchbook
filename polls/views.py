from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, View, UpdateView, DeleteView, ListView, TemplateView



from .models import Poll, Choice, VoteData
from .forms import PollForm, ChoiceForm

# Create your views here.

User = get_user_model()


class PollList(ListView):
    model = Poll
    paginate_by = 10
    template_name = 'polls/poll_list.html'



class PollDetail(LoginRequiredMixin ,DetailView):
    model = Poll
    template_name='polls/poll_detail.html'
    context_object_name = 'poll'


    def post(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        choice_id = request.POST.get('choice')
        choice = get_object_or_404(Choice, pk=choice_id)
        choice.upvote()
        vote_data = VoteData(poll=poll, user=request.user, choice=choice.choice_text)
        vote_data.save()
        return redirect('poll:poll_result', pk=pk)
    
    # def get_context_data(self, **kwargs):
    #     poll_permission = self.model.get_vote_permission(self.request)
    #     kwargs.update({
    #         'poll_permission': poll_permission
    #     })
    #     return super().get_context_data(**kwargs)

    def get_context_data(self, **kwargs):
        context = dict()
        user = get_user(self.request)
        if user.is_authenticated:
            if self.object.voter.all().filter(email=user.email).exists():
                poll_permission = False
            else:
                poll_permission = True
            context.update({'poll_permission': poll_permission})
        context.update(kwargs)
        return super().get_context_data(**context)



class PollCreate(LoginRequiredMixin ,View):
    login_url = reverse_lazy('student:login')
    model = Poll
    template_name = 'polls/poll_form.html'
    form_class = PollForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={
            'author': request.user
        })
        ChoiceInlineFormset = inlineformset_factory(
            Poll, Choice, form=ChoiceForm, min_num=2, max_num=6,
            validate_min=True, validate_max=True, extra=2
        )
        formset = ChoiceInlineFormset()
        return render(request, self.template_name,{
            'form':form,
            'formset':formset
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        ChoiceInlineFormset = inlineformset_factory(
            Poll, Choice, form=ChoiceForm, min_num=2, max_num=6, validate_min=True, validate_max=True)
        formset = ChoiceInlineFormset(request.POST)
        if all([form.is_valid(), formset.is_valid()]):
            poll = form.save(commit=False)
            poll.author = get_user(request)
            poll.save()
            for inline_form in formset:
                choice = inline_form.save(commit=False)
                choice.question = poll
                if choice.choice_text != '':
                    choice.save()
            return redirect(poll)
        else:
            return render(request, self.template_name, {
                'form':form,
                'formset':formset
            })

        


class PollDelete(LoginRequiredMixin, DeleteView):
    model = Poll
    login_url = reverse_lazy('student:login')
    template_name = 'polls/poll_confirm_delete.html'
    success_url = reverse_lazy('poll:poll_list')

class PollResult(LoginRequiredMixin, TemplateView):
    template_name = 'polls/poll_result.html'

    def get_context_data(self, **kwargs):
        user = get_user(self.request)
        poll_pk = self.kwargs.get('pk')
        poll = get_object_or_404(Poll, pk=poll_pk)
        choices = poll.choices.all()
        choice_lable = []
        vote_data = []
        for choice in choices:
            choice_lable.append(choice.choice_text)
            vote_data.append(choice.vote)
        if poll.voter.all().filter(email=user.email).exists():
            result_permission = True
        else:
            result_permission = False

        kwargs.update({
            'poll': poll,
            'choice_label': choice_lable,
            'vote_data': vote_data,
            'result_permission': result_permission
        })
        return super().get_context_data(**kwargs)
        

class ChoiceCreate(LoginRequiredMixin ,CreateView):
    model = Choice
    form_class = ChoiceForm
    login_url = reverse_lazy('student:login')

    def get_initial(self):
        poll = get_object_or_404(Poll, pk=self.kwargs.get('poll_pk'))
        initial = {
            'question': poll
        }
        initial.update(self.initial)
        return initial
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            poll = get_object_or_404(Poll, pk=request.POST.get('question'))
            choice = form.save(commit=False)
            choice.question = poll
            choice.save()
            return redirect(poll.get_absolute_url())
        else:
            return self.form_invalid(form)



@login_required(login_url=reverse_lazy('student:login'))
def edit_poll(request, pk):
    ChoiceInlineFormSet = inlineformset_factory(Poll, Choice, form=ChoiceForm, min_num=2, max_num=6, validate_max=True, validate_min=True, extra=1)
    poll = get_object_or_404(Poll, pk=pk)
    if request.method == 'POST':
        formset = ChoiceInlineFormSet(request.POST, instance=poll)
        form = PollForm(request.POST, instance=poll)
        if all([formset.is_valid() , form.is_valid()]):
            form.save()
            formset.save()
            return redirect(reverse('poll:poll_detail', kwargs={'pk':poll.pk}))
    else:
        form = PollForm(instance=poll)
        formset = ChoiceInlineFormSet(instance=poll)
    return render(request, 'polls/poll_form_update.html',
                  context={
                      'form': form,
                      'formset': formset,
                      'poll': poll
                  })


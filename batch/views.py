from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import BatchModel
# Create your views here.


class BatchList(ListView):
    model = BatchModel
    context_object_name = 'batches'
    template_name = 'batch/batch_list.html'
    paginate_by = 20


class BatchDetailView(DetailView):
    model = BatchModel
    context_object_name = 'batch'
    template_name = "batch/batch_detail.html"   

    def get_object(self, *args, **kwargs):
        department = self.kwargs.get('department')
        year =  self.kwargs.get('year')
        section = self.kwargs.get('section')
        return self.model.objects.get(
            department__iexact=department,
            year = year,
            section = section
        )





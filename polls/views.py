from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


from .forms import LabelForm

from .models import Choice, Question, Conversation, Label


# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'

#     def get_queryset(self):
#         """
#         Return the last five published questions (not including those set to be
#         published in the future).
#         """
#         return Question.objects.filter(
#             labeled=False
#         )
class IndexView(generic.ListView):
    """CBV to render the index view
    """
    model = Question
    paginate_by = 10
    context_object_name = 'questions'
    template_name = 'polls/index.html'
    ordering = '-pub_date'

    def get_context_data(self, *args, **kwargs):
        context = super(
            IndexView, self).get_context_data(*args, **kwargs)
        noans = Question.objects.filter(
            labeled=False
            )
        context['totalcount'] = Question.objects.count()
        paginator = Paginator(noans, 10)
        page = self.request.GET.get('noans_page')
        context['active_tab'] = self.request.GET.get('active_tab', 'latest')
        tabs = ['latest', 'unans', 'reward']
        context['active_tab'] = 'latest' if context['active_tab'] not in\
            tabs else context['active_tab']
        try:
            noans = paginator.page(page)

        except PageNotAnInteger:
            noans = paginator.page(1)

        except EmptyPage:  # pragma: no cover
            noans = paginator.page(paginator.num_pages)

        context['totalnoans'] = paginator.count
        context['noans'] = noans
        return context

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            labeled=False
        )


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    context_object_name = 'question'
    def get_context_data(self, **kwargs):
        conv = self.object.conversation_set.all().order_by('roundid')
        label = self.object.label_set.all().order_by('roundid')
        context = super(DetailView, self).get_context_data(**kwargs)
        context['conv'] = list(conv)
        context['label']=list(label)
        noans = Question.objects.filter(
            labeled=False
            )
        nextpk = [o for o in noans if o.id != self.object.id][0].id
        context['message'] = nextpk
        context['nextpk']=nextpk
        return context

    def get_object(self):
        question = super(DetailView, self).get_object()
        return question

    # def get_queryset(self):
    #     """
    #     Excludes any questions that aren't published yet.
    #     """
    #     return Question.objects.filter(pub_date__lte=timezone.now())



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    label = get_object_or_404(Label, pk=question_id)
    form = LabelForm(request.POST)
    if form.is_valid():
        keywords = form.cleaned_data['label_text']
        label.label_text = keywords
        label.save()
        labels = label.question.label_set.all()
        Q = label.question
        Q.labeled=len([l for l in labels if l.label_text=='NA'])==0
        Q.save()
        return HttpResponseRedirect(reverse('polls:detail', args=(label.question.id,)))
    
    return HttpResponseRedirect(reverse('polls:detail', args=(label.question.id,)))

from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView
from django.urls.base import reverse_lazy
from typing import Any
from django.shortcuts import get_object_or_404
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.db import models

from .models import Question, Theme, TestEntry
from .utils import retrieve_random_questions


class ThemeListView(ListView):
    queryset = Theme.objects.select_related('parent')
    template_name = 'tests_app/themes.html'
    context_object_name = 'theme_list'


class ThemeDetailView(ListView):
    model = Question
    template_name = 'tests_app/questions.html'
    context_object_name = 'question_list'

    def get_queryset(self) -> models.QuerySet[Any]:
        theme = get_object_or_404(Theme, name=self.kwargs['theme'])
        return Question.objects.select_related('theme').filter(theme=theme)


class QuestionListView(ListView):
    queryset = Question.objects.select_related('theme')
    template_name = 'tests_app/questions.html'
    context_object_name = 'question_list'


class QuestionCreateView(CreateView):
    model = Question
    fields = ['question', 'answer', 'theme']
    template_name = 'tests_app/question_add.html'
    success_url = reverse_lazy('home')

    def get_success_url(self) -> str:
        if self.request.POST.get("_continue"):
            return reverse_lazy('question_add')
        return super().get_success_url()


class QuestionRandomListView(ListView):
    model = Question
    template_name = 'tests_app/questions.html'
    context_object_name = 'question_list'
    question_quantity = 5

    def get_queryset(self) -> models.QuerySet[Any]:
        return retrieve_random_questions(self.question_quantity)


class TestCreateView(CreateView):
    model = TestEntry
    fields = ['questions']
    template_name = 'tests_app/test_create.html'
    success_url = reverse_lazy('home')


class TestListView(ListView):
    model = TestEntry
    # queryset = TestEntry.objects.prefetch_related('questions')
    queryset = TestEntry.objects.prefetch_related(
        models.Prefetch('questions__theme'))
    template_name = 'tests_app/tests.html'
    context_object_name = 'test_list'
    ordering = '-id'


class TestDetailView(DetailView):
    model = TestEntry
    template_name = 'tests_app/test_detail.html'
    context_object_name = 'question'
    
    def get_object(self) -> models.Model:
        pk = self.kwargs.get(self.pk_url_kwarg)
        # questions = self.model.objects.filter(id=pk).prefetch_related(
        #     models.Prefetch('questions__theme')
        # )
        questions = self.model.objects.filter(id=pk).prefetch_related('questions')
        if not questions:
            raise Http404
        questions = questions[0].questions.all()

        self.q_len = len(questions)
        if self.q < 1 or self.q > self.q_len:
            raise Http404
        return questions[self.q-1]

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        q = request.GET.get('q')
        if q is None:
            q = 1
        try:
            q = int(q)
        except (ValueError, TypeError) as error:
            print(error)
            raise Http404
        
        self.q = q
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data['pk'] = self.kwargs.get(self.pk_url_kwarg)
        data['next'] = self.q + 1
        data['last_q'] = True if self.q == self.q_len else False
        return data


class TestCreateRandomView(View):
    question_quantity = 5
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        test = TestEntry.objects.create()
        questions = retrieve_random_questions(self.question_quantity)
        for q in questions:
            test.questions.add(q)
        test.save()

        return HttpResponseRedirect(reverse_lazy('test_list'))

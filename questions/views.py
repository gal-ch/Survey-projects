from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, FormView, DetailView
from django.views.generic.edit import ModelFormMixin, FormMixin
from accounts.models import MyUser
from questions.forms import UserResponseForm
from questions.models import Question, Answer, UserAnswer


class QuestionDetailView(FormMixin, DetailView):
    template_name = "questions/question_set.html"
    model = Question
    form_class = UserResponseForm

    def get_success_url(self):
        current_question = self.get_object().pk
        next_question = current_question + 1
        return reverse('question', kwargs={'pk': next_question})

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if not form.is_valid():
            return self.get(request, self.object.pk)
        form.instance.user = request.user
        print(form.instance.user)
        form.instance.question = self.object
        print(form.instance.question)
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self, *args, **kwargs):
        initial = super(QuestionDetailView, self).get_initial()
        initial['pk'] = self.get_object().pk
        self.form_class(initial)
        return initial










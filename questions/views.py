from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, FormView, DetailView
from django.views.generic.edit import FormMixin
from questions.forms import UserResponseForm
from questions.models import Question, Answer


class QuestionDetailView(FormMixin, DetailView):
    template_name = "questions/question_set.html"
    model = Question
    form_class = UserResponseForm

    def get_success_url(self):
        next_question = Question.objects.all().order_by('-timestemp').first()
        return reverse('question', kwargs={'pk': next_question.pk})

    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        ans = form.cleaned_data['answer_id']
        print(ans)
        return super().form_valid(form)


# class QuestionDetailView(DetailView):
#     template_name = "questions/question_set.html"
#     model = Question
#
#     def get_context_data(self, **kwargs):
#         context = super(QuestionDetailView, self).get_context_data(**kwargs)
#         context['form'] = UserResponseForm()
#         return context
#
#     def post(self, request, pk):
#         form = UserResponseForm(request.POST)
#         # if form.is_valid():
#         next_question = Question.objects.all().order_by('-timestemp').first()
#         return redirect('question', pk=next_question.pk)



# def questionFormView(request):
#     if request.user.is_authenticated:
#         form = UserResponseForm(request.POST or None)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             question_id = form.cleaned_data.get('question_id')
#             answer_id = form.cleaned_data.get('answer_id')
#             print(answer_id)
#             question_instance = Question.objects.get(id=question_id)
#             answer_instance = Answer.objects.get(id=answer_id)
#         queryset = Question.objects.all()
#         instance = queryset[0]
#         context = {
#             'form':form,
#             'instance':instance,
#         }
#         return render(request,"questions/question_set.html", context)
#     else:
#         raise Http404("No MyModel matches the given query.")









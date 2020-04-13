from django.urls import reverse
from django.views.generic import ListView, FormView, DetailView
from django.views.generic.edit import FormMixin
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
        try:
            context['user_ans_prv'] = UserAnswer.objects.get(user=self.request.user, question=self.object)
        except UserAnswer.DoesNotExist:
            context['user_ans_prv'] = None
        except UserAnswer.MultipleObjectsReturned:
            context['user_ans_prv'] = UserAnswer.objects.filter(user=self.request.user, question=self.object)[0]
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # to fix - i saved it twice
        ans_user = UserAnswer()
        question_id = form.cleaned_data.get('question_id')
        user_answer_id = form.cleaned_data.get('answer_id')
        user_importance_level = form.cleaned_data.get('user_importance_level')
        other_user_answer_id = form.cleaned_data.get('other_user_answer_id')
        other_user_importance_level = form.cleaned_data.get('other_user_importance_level')
        ans_user.user = MyUser.objects.get(pk=self.request.user.pk)
        ans_user.question = Question.objects.get(id=question_id)
        ans_user.user_answer = Answer.objects.get(id=user_answer_id)
        ans_user.user_importance_level = user_importance_level
        if other_user_answer_id != -1:
            ans_user.other_user_answer = Answer.objects.get(id=other_user_answer_id)
            ans_user.other_user_importance_level = other_user_importance_level
        else:
            ans_user.other_user_answer = None
            ans_user.other_user_importance_level = 'Not important'
        ans_user.save()
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









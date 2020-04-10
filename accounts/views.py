# signup -> verficatiion email-> create profile
# social signup -> create profile
from django.contrib.auth import login
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import View, UpdateView, TemplateView, DetailView
from .forms import SignUpForm, ProfileForm
from .models import MyUser


class HomePageView(TemplateView):
    template_name = 'home.html'


# Sign Up View
class SignUpView(View):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        # user = self.get_object()
        if form.is_valid():
            user = form.save(commit=False)
            print('user', user)
            user.is_active = True
            user.save()
            login(request, user)

            # current_site = get_current_site(request)
            # subject = 'Activate Your MySite Account'
            # message = render_to_string('emails/account_activation_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # user.email_user(subject, message)

            # messages.success(request, ('Please Confirm your email to complete registration.'))

           # return redirect('login')
            return redirect('accounts:profile-create', pk=user.pk)

        return render(request, self.template_name, {'form': form})


# class ActivateAccount(View):
#     def get(self, request, uidb64, token, *args, **kwargs):
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
#
#         if user is not None and account_activation_token.check_token(user, token):
#             user.is_active = True
#             user.profile.email_confirmed = True
#             user.save()
#             login(request, user)
#             messages.success(request, ('Your account have been confirmed.'))
#             return redirect('accounts:profile', pk=user.pk)
#         else:
#             messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
#             return redirect('accounts:home')


class ProfileUpdateView(UpdateView):
    model = MyUser
    form_class = ProfileForm
    template_name = 'accounts/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk == self.get_object().pk:
            return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)
        return redirect(reverse('accounts:home'))

    def get_success_url(self, **kwargs):
        print(self.object.pk)
        if kwargs != None:
            return reverse_lazy('accounts:profile-detail', kwargs={'pk': self.object.pk})


class ProfileDetailView(DetailView):
    model = MyUser
    template_name = 'accounts/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        return context

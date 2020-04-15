from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View, UpdateView, TemplateView, DetailView, CreateView
from .forms import SignUpForm, ProfileForm
from .models import MyUser, Profile


class LoginRequireMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_profile == False:
            return redirect('accounts:profile-create', pk=request.user.pk)
        return super(LoginRequireMixin, self).dispatch(request, *args, **kwargs)


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
            return redirect('accounts:profile-create')
        return render(request, self.template_name, {'form': form})


class ProfileUpdateView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile.html'

    def dispatch(self, request, *args, **kwargs):
        user_admin = MyUser.objects.get(email=request.user)
        print(user_admin.hasProfile)
        profile = user_admin.hasProfile
        if profile:
            return redirect(reverse('home'))
        return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        new_profile = form.save()
        return redirect(reverse('accounts:profile-detail', kwargs={'pk': new_profile.pk}))


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'

    def dispatch(self, request, *args, **kwargs):
        user_admin = MyUser.objects.get(email=request.user)
        print(request.user)
        print(user_admin.hasProfile)
        profile = user_admin.hasProfile
        if profile and request.user.is_authenticated:
            return super(ProfileDetailView, self).dispatch(request, *args, **kwargs)
        return redirect('accounts:profile-create')

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        return context




    # def dispatch(self, request, *args, **kwargs):
    #     user_admin = MyUser.objects.get(email=request.user)
    #     profile = user_admin.hasProfile
    #     if profile == False:
    #         return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)
    #     return redirect(reverse('home'))
    #
    # def get_success_url(self, **kwargs):
    #     print(self.object.pk)
    #     if kwargs != None:
    #         return reverse_lazy('accounts:profile-detail', kwargs={'pk': self.object.pk})
    #
    # def form_valid(self, form):
    #     form = self.get_form()
    #     if not form.is_valid():
    #         return self.get(self.object.pk)
    #     form.instance.user = self.request.user
    #     print(form.instance.user)
    #     form.save()
    #     return HttpResponseRedirect(self.get_success_url())
        # self.success_url = reverse('accounts:profile-detail', kwargs={'pk': self.request.user.pk})

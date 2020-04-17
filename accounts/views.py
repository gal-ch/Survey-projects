from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View, UpdateView, TemplateView, DetailView, CreateView, ListView
from matches.models import Match
from .forms import SignUpForm, ProfileForm, JobFormset
from .models import MyUser, Profile, UserJob

User = get_user_model()


class LoginRequireMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_profile == False:
            return redirect('accounts:profile-create', pk=request.user.pk)
        return super(LoginRequireMixin, self).dispatch(request, *args, **kwargs)


class HomePageView(TemplateView):
    template_name = 'home.html'


class MatchesList(ListView):
    template_name = 'accounts/matches_list.html'

    def get_queryset(self):
        matches = Match.objects.get_percent_matches(self.request.user)
        ''' list view that show the user matches '''
        return matches


# Sign Up View # not active
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


class ProfileDetail(DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'

    def dispatch(self, request, *args, **kwargs):
        user_admin = MyUser.objects.get(email=request.user)
        print(request.user)
        print(user_admin.hasProfile)
        profile = user_admin.hasProfile
        if profile and request.user.is_authenticated:
            return super(ProfileDetail, self).dispatch(request, *args, **kwargs)
        return redirect('accounts:profile-create')

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        profile = self.get_object()
        print(profile)
        print(profile)
        user_profile = get_object_or_404(Profile, user_id=profile.user_id)
        user_instance = get_object_or_404(User, id=profile.user_id)
        login_user = get_object_or_404(User, email=self.request.user)
        # display user match in context to the connected user
        match, match_created = Match.objects.get_or_create_match(user_a=user_instance, user_b=login_user)
        context['match'] = match
        print(context['match'])
        # get user jobs info
        jobs = UserJob.objects.filter(user=profile.user_id)
        context['jobs'] = jobs
        return context


class ProfileCreate(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_job_form.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['job_form'] = JobFormset(self.request.POST)
        else:
            context['job_form'] = JobFormset(instance=self.object)
        return context

    def dispatch(self, request, *args, **kwargs):
        user_admin = MyUser.objects.get(email=request.user)
        print(user_admin.hasProfile)
        profile = user_admin.hasProfile
        if profile:
            return redirect(reverse('home'))
        return super(ProfileCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print('user', self.request.user)
        # print('self.object', self.object.user)
        context = self.get_context_data()
        job_form = context['job_form']
        user_admin = MyUser.objects.get(email=self.request.user)
        if job_form.is_valid():
            self.object.user = self.request.user
            self.object = form.save()
            job_form.instance = self.object
            job_form.instance.user = self.request.user
            job_form.save()
            user_admin.hasProfile = True
            user_admin.save()
            return HttpResponseRedirect(reverse('accounts:profile-detail', kwargs={'pk': self.request.user.id}))
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProfileUpdate(UpdateView):
        model = Profile
        form_class = ProfileForm
        template_name = 'accounts/profile_job_form.html'

        def dispatch(self, request, *args, **kwargs):
            obj = self.get_object()
            if request.user == obj.user:
                return super(ProfileUpdate, self).dispatch(request, *args, **kwargs)
            return redirect(reverse('home'))

        def get_context_data(self, **kwargs):
            context = super(ProfileUpdate, self).get_context_data(**kwargs)
            if self.request.POST:
                context['profile_form'] = ProfileForm(self.request.POST, instance=self.object)
                context['job_form'] = JobFormset(self.request.POST, instance=self.object)
            else:
                context['profile_form'] = ProfileForm(instance=self.object)
                context['job_form'] = JobFormset(instance=self.object)
            return context

        def form_valid(self, form):
            context = self.get_context_data()
            profile_form = context['profile_form']
            job_form = context['job_form']
            if job_form.is_valid() and profile_form.is_valid():
                self.object = form.save()
                profile_form.instance.user = self.request.user
                profile_form.instance = self.object
                profile_form.save()
                job_form.instance.user = self.request.user
                job_form.instance = self.object
                job_form.save()

            return self.render_to_response(self.get_context_data(form=form))


# only profile info (without a job adding)
# class ProfileCreateView(CreateView):
#     model = Profile
#     form_class = ProfileForm
#     template_name = 'accounts/profile.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         user_admin = MyUser.objects.get(email=request.user)
#         print(user_admin.hasProfile)
#         profile = user_admin.hasProfile
#         if profile:
#             return redirect(reverse('home'))
#         return super(ProfileCreateView, self).dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         user_admin = MyUser.objects.get(email=request.user)
#         if form.is_valid():
#             self.new_profile = form.save(commit=False)
#             form.instance.user_id = self.request.user.pk
#             self.new_profile = form.save()
#             user_admin.hasProfile = True
#             user_admin.save()
#             return HttpResponseRedirect(reverse('accounts:profile-detail', kwargs={'pk': self.new_profile.id}))
#         else:
#             return redirect(reverse('home'))

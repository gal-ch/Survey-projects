from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View, UpdateView, TemplateView, DetailView, CreateView, ListView
from matches.models import Match
from .forms import SignUpForm, ProfileForm, JobForm, JobFormset
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
        ''' list view that show the user matches '''
        log_user = self.request.user
        queryset_not_filter = Match.objects.matches_all(self.request.user).order_by('-match_decimal')
        queryset = []
        for match in queryset_not_filter:
            if match.user_a == log_user and match.user_b != log_user:
                match_to_list = [match.user_b, match.get_percent]
                queryset.append(match_to_list)
            if match.user_b == log_user and match.user_a != log_user:
                match_to_list = [match.user_a, match.get_percent]
                queryset.append(match_to_list)
            else:
                pass
        return queryset


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
        profile = self.get_object()
        user_profile = get_object_or_404(Profile, id=profile.pk)
        user_instance = get_object_or_404(User, email=user_profile)
        login_user = get_object_or_404(User, email=self.request.user)
        # display user match in context to the connected user
        match, match_created = Match.objects.get_or_create_match(user_a=user_instance, user_b=login_user)
        context['match'] = match
        # get user jobs info
        # jobs = UserJob.objects.get(user=profile.user_id)
        # context['jobs'] = jobs
        return context


class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile.html'

    def dispatch(self, request, *args, **kwargs):
        user_admin = MyUser.objects.get(email=request.user)
        print(user_admin.hasProfile)
        profile = user_admin.hasProfile
        if profile:
            return redirect(reverse('home'))
        return super(ProfileCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user_admin = MyUser.objects.get(email=request.user)
        if form.is_valid():
            self.new_profile = form.save(commit=False)
            form.instance.user_id = self.request.user.pk
            self.new_profile = form.save()
            user_admin.hasProfile = True
            user_admin.save()
            return HttpResponseRedirect(reverse('accounts:profile-detail', kwargs={'pk': self.new_profile.id}))
        else:
            return redirect(reverse('home'))


class ProfileUpdate(UpdateView):
        model = Profile
        form_class = ProfileForm
        template_name = 'accounts/profile.html'

        def dispatch(self, request, *args, **kwargs):
            obj = self.get_object()
            if request.user == obj.user:
                return super(ProfileUpdate, self).dispatch(request, *args, **kwargs)
            return redirect(reverse('home'))

        def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            form = self.get_form()
            if not form.is_valid():
                return self.get(request, self.object.pk)
            form.save()
            return redirect(reverse('home'))


class JobCreateView(CreateView):
    model = UserJob
    form_class = JobForm
    template_name = 'accounts/job_form.html'

    def get_context_data(self, **kwargs):
        context = super(JobCreateView, self).get_context_data(**kwargs)
        context['formset'] = JobFormset(queryset=UserJob.objects.filter(user=self.request.user))
        return context

    def post(self, request, *args, **kwargs):
        formset = JobFormset(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        user_profile = Profile.objects.get(user_id=self.request.user.pk)
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = self.request.user
            instance.save()
        return HttpResponseRedirect(reverse('accounts:profile-detail', kwargs={'pk': user_profile.id}))


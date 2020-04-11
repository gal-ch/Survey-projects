from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import accounts
from accounts.views import HomePageView
from questions.views import QuestionDetailView

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question'),
    path('admin/', admin.site.urls),

    path('', include('accounts.urls')),
    url(r'^accounts/', include('allauth.urls')),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True,
                                                template_name='account/login.html'),
                                                 name='login'),


]

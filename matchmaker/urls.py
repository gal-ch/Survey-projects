
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import accounts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html'),
         name='login'),

]

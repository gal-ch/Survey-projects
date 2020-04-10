
from django.urls import path
from accounts.views import (
    SignUpView,
    ActivateAccount,
    ProfileView,
    HomePageView,
)


app_name = 'accounts'
urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

]






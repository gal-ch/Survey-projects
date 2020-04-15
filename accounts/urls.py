from django.conf.urls import url
from django.urls import path
from accounts.views import (
    SignUpView,
    # ActivateAccount,
    ProfileCreateView,
    HomePageView,
    ProfileDetailView, ProfileUpdate)


app_name = 'accounts'
urlpatterns = [

    # path('home/', HomePageView.as_view(), name='home'),
    # path('signup/', SignUpView.as_view(), name='signup'),
    path('profile-create/', ProfileCreateView.as_view(), name='profile-create'),
    path('profile-detail/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile-update/<int:pk>/', ProfileUpdate.as_view(), name='profile-update'),
    # path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),


]






from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect


class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
            path = "/profile-create/{pk}"
            return path.format(pk=request.user.pk)
        # if request.user.has_profile == False:
        #     path = "/profile-create/{pk}"
        #     return path.format(pk=request.user.pk)
        # else:
        #     path = "/home/"
        #     return path






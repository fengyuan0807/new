from django.shortcuts import redirect
from django.urls import reverse

# redirect()
# reverse()
from django.views import View

from users.models import User


class UserNameCount(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()

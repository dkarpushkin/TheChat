from django.contrib.auth import views, login
from django.http import HttpResponseRedirect

from Chat.forms import AuthNoPasswordForm


class LoginNoPassword(views.LoginView):
    form_class = AuthNoPasswordForm

    def form_valid(self, form):
        if form.create_user:
            form.save()

        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())
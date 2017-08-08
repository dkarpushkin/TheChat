from django import forms
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User


UserModel = get_user_model()

class AuthNoPasswordForm(forms.ModelForm):
    error_messages = {
        'invalid_user': 'This user is not allowed to login here'
    }

    default_password = 'default_password'   #   for passwordless login

    class Meta:
        model = UserModel
        fields = ("username",)
        field_classes = {'username': UsernameField}

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        self.create_user = False
        super(AuthNoPasswordForm, self).__init__(*args, **kwargs)

        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean(self):
        username = self.cleaned_data.get('username')

        if username is not None:
            self.user_cache = authenticate(username=username, password=self.default_password)
            #self.user_cache = User.objects.filter(username=username).first()
            if self.user_cache is not None:
                if self.user_cache.is_staff or self.user_cache.is_superuser:
                    raise forms.ValidationError(
                        self.error_messages['invalid_user'],
                        code='invalid_user',
                        params={'username': self.username_field.verbose_name},
                    )
            else:
                self.create_user = True

        return self.cleaned_data

    def save(self, commit=True):
        self.user_cache = super(AuthNoPasswordForm, self).save(commit=False)
        self.user_cache.set_password(self.default_password)
        if commit:
            self.user_cache.save()
        return self.user_cache

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

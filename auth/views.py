from django.contrib.auth import authenticate, login
from django.forms import Form, ModelForm
from django.views.generic import FormView

from .forms import CustomUserCreationForm


class RegisterView(FormView):
    template_name = 'auth/register.html'
    form_class = CustomUserCreationForm
    success_url = "/"

    def form_valid(self, form: ModelForm):
        """Security check complete. Log the user in."""
        user = form.save()
        # log the user in
        user = authenticate(username=user.username, password=form.cleaned_data['password1'])
        login(self.request, user)
        return super().form_valid(form)

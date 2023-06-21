from django.contrib.auth import authenticate, login
from django.views.generic import FormView

from .forms import CustomUserCreationForm


class RegisterView(FormView):
    template_name = 'authentication/register.html'
    form_class = CustomUserCreationForm
    success_url = "/"

    def form_valid(self, form: CustomUserCreationForm):
        """Security check complete. Log the user in."""
        user = form.save()

        # log the user in
        user = authenticate(username=user.username, password=form.cleaned_data['password1'])
        login(self.request, user)
        return super().form_valid(form)

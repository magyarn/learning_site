from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic

from . import forms

class LoginView(generic.FormView):
  form_class = AuthenticationForm
  template_name = "accounts/login.html"

  def get_success_url(self):
    return reverse_lazy("courses:my_courses", kwargs={'userId': self.request.user.pk})

  def get_form(self, form_class=None):
    if form_class is None:
      form_class = self.get_form_class()
    return form_class(self.request, **self.get_form_kwargs())

  def form_valid(self, form):
    login(self.request, form.get_user())
    return super().form_valid(form)

class LogoutView(generic.RedirectView):
  url = reverse_lazy("courses:home")

  def get(self, *args, **kwargs):
    logout(self.request)
    return super().get(self.request, *args, **kwargs)

class SignupView(generic.CreateView):
  form_class = forms.CustomUserCreationForm
  success_url = reverse_lazy("accounts:login")
  template_name = "accounts/signup.html"



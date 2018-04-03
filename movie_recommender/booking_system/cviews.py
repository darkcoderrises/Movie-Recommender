from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import generic

from .forms import LoginForm
class LoginView(generic.FormView):
    form_class = LoginForm
    success_url = reverse_lazy('index')
    template_name = 'registration/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)



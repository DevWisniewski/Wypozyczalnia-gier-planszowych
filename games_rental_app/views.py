from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, FormView, ListView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .forms import (LoginForm, AddUserForm,)

User = get_user_model()

class LoginView(FormView):
    template_name = "games_rental_app/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("my_account")

    def form_valid(self, form):
        user = form.user
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(RedirectView):
    url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class AddUserView(CreateView):
    template_name = "games_rental_app/add_user.html"
    model = User
    form_class = AddUserForm
    success_url = reverse_lazy("login")


class MyAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'games_rental_app/my_account.html'

    def get_context_data(self, **kwargs):
        context = super(MyAccountView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class StaticGameDetailsView(TemplateView):
    template_name = 'games_rental_app/static_game_details.html'

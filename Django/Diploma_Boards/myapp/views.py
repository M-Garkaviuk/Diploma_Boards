# myapp.views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, CreateView

from myapp.forms import UserForm
from myapp.models import Card


def main(request):
    return HttpResponse("Hey! It's your main view!!")


class TaskListView(ListView):
    model = Card
    template_name = 'index.html'
    login_url = 'login/'
    # extra_context = {'purchase_form': PurchaseCreationForm()}


class Login(LoginView):
    success_url = '/'
    template_name = 'login.html'

    def get_success_url(self):
        return self.success_url


class Register(CreateView):
    form_class = UserForm
    template_name = 'registration_page.html'
    success_url = '/'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'

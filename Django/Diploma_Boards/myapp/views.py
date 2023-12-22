# myapp.views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic import ListView, CreateView
from django.conf import settings
from myapp.forms import UserForm, CardForm
from myapp.models import Card
from Diploma_Boards.settings import BOARD_STATUSES
from django.contrib import messages


class CardListView(ListView):
    model = Card
    template_name = 'index.html'
    login_url = 'login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['BOARD_STATUSES'] = BOARD_STATUSES
        return context


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


class UserLoginRequiredMixin:
    pass


class CardCreateView(UserLoginRequiredMixin, CreateView):
    template_name = 'card_create.html'
    login_url = 'login/'
    http_method_names = ['get', 'post']
    form_class = CardForm
    success_url = '/'

    def form_valid(self, form):
        user = self.request.user
        card = form.save(commit=False)
        card.created_by = user
        card.save()

        messages.success(self.request, f'You have successfully created a new card "{card.title}"! Thank you!')

        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # card_title = form.cleaned_data.get('card_title')
        # messages.success(self.request, f'Card "{card_title}" created successfully.')
        return response

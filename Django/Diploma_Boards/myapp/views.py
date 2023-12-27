# myapp.views
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import authenticate
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse
from myapp.forms import UserForm, CardCreateForm, CardEditForm
from myapp.models import Card
from Diploma_Boards.settings import BOARD_STATUSES
from django.contrib import messages

# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView


class AdminLoginRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserLoginRequiredMixin:
    pass


class CardListView(ListView):
    model = Card
    template_name = 'index.html'
    login_url = 'login/'
    context_object_name = 'cards'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['BOARD_STATUSES'] = BOARD_STATUSES

        for card in context['cards']:

            card.user_can_move_to_next_status = card.user_can_move_to_next_status()
            card.user_can_move_to_previous_status = card.user_can_move_to_previous_status()
            card.manager_can_move_to_next_status = card.manager_can_move_to_next_status()
            card.manager_can_move_to_previous_status = card.manager_can_move_to_previous_status()


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


class Logout(LogoutView):
    next_page = '/'


class CardCreateView(UserLoginRequiredMixin, CreateView):
    template_name = 'card_create.html'
    login_url = 'login/'
    http_method_names = ['get', 'post']
    form_class = CardCreateForm
    success_url = '/'

    def form_valid(self, form):
        user = self.request.user
        card = form.save(commit=False)
        card.created_by = user
        card.save()

        messages.success(self.request, f'You have successfully created a new card "{card.title}"! Thank you!')

        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        return response


class CardUpdateView(UserLoginRequiredMixin, UpdateView):
    model = Card
    form_class = CardEditForm
    template_name = 'card_update.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            card = form.save(commit=False)
            card.save()
            messages.success(self.request, f'Card "{card.title}" updated successfully.')
            return super().form_valid(form)

    def get_success_url(self):
        return reverse("index")


class StatusChangeView(LoginRequiredMixin, View):
    model = Card
    context_object_name = 'cards'

    def post(self, request, pk):
        try:
            card = Card.objects.get(pk=pk)
        except Card.DoesNotExist:
            return HttpResponseBadRequest("The card not found")

        action = request.POST.get('action')

        if action == 'next':
            card.set_next_status()

        elif action == 'previous':
            card.set_previous_status()

        return HttpResponseRedirect('/')


class CardDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        try:
            card = Card.objects.get(pk=pk)
            card.delete()

        except Card.DoesNotExist:
            return HttpResponseBadRequest('The card not found')
        messages.success(self.request, f'The card "{card.title}" was deleted')
        return HttpResponseRedirect('/')

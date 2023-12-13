from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from myapp.models import User, Card


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = "__all__"




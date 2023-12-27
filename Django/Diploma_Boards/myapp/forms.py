from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from myapp.models import User, Card


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class CardCreateForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('title', 'content')


class CardEditForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['assignee'].required = False

    class Meta:
        model = Card
        fields = ('assignee', 'title', 'content')

    def clean_assignee(self):
        assignee = self.cleaned_data.get('assignee')
        user = self.request.user
        created_by = self.instance.created_by

        if user.is_manager:
            return assignee

        if user == created_by and (assignee == created_by or assignee is None):
            return assignee

        if assignee == user or assignee is None:
            return assignee

        raise forms.ValidationError("You are not allowed to assign this card to the selected user.")



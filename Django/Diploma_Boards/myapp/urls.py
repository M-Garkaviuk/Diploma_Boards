# myapp.urls
from django.urls import path
from myapp.views import (CardListView,
                         Register,
                         Login,
                         Logout,
                         CardCreateView)


urlpatterns = [
    path('', CardListView.as_view(), name='index'),
    path('card/create', CardCreateView.as_view(), name='card-create'),
    path('registration/', Register.as_view(), name='registration'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

]
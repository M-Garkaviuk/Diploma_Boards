# myapp.urls
from django.urls import path
from myapp.views import TaskListView, Register, Login, Logout


urlpatterns = [
    path('', TaskListView.as_view(), name='index'),
    path('registration/', Register.as_view(), name='registration'),
    path('registration/', Register.as_view(), name='registration'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

]
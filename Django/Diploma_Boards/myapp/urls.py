# myapp.urls

from django.urls import path, include
from rest_framework import routers

from myapp.API.resourses import CardViewSet, CustomAuthToken
from myapp.views import (CardListView,
                         Register,
                         Login,
                         Logout,
                         CardCreateView,
                         CardUpdateView,
                         CardDeleteView,
                         StatusChangeView,
                         )
router = routers.DefaultRouter()
router.register(r'card', CardViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', CustomAuthToken.as_view()),
    path('', CardListView.as_view(), name='index'),
    path('card/create/', CardCreateView.as_view(), name='card-create'),
    path('card/<int:pk>/update/', CardUpdateView.as_view(), name='card-update'),
    path('card/<int:pk>/status/', StatusChangeView.as_view(), name='status-update'),
    path('card/<int:pk>/delete/', CardDeleteView.as_view(), name='card-delete'),
    path('registration/', Register.as_view(), name='registration'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

]

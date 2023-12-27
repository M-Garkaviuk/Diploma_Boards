import datetime
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from Diploma_Boards import settings
from myapp.API.authentication import TokenExpiration
from myapp.API.serializers import CardViewSerializer
from myapp.models import Card


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        now = datetime.datetime.now()
        Token.objects.filter(user=user, created__lt=now - datetime.timedelta(seconds=settings.TOKEN_EXPIRATION)).delete()

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardViewSerializer
    authentication_classes = [TokenExpiration]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class CardStatusSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['=status']



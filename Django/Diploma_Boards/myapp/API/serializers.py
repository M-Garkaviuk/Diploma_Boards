from rest_framework import serializers

from Diploma_Boards.settings import BOARD_STATUSES
from myapp.models import Card, User
from django.conf.urls import include
from rest_framework import routers, serializers, viewsets


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)


class CardSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=True, allow_blank=False, max_length=255)
    # content = serializers.CharField(required=True, allow_blank=False, max_length=1000)
    # status = serializers.ChoiceField(choices=BOARD_STATUSES, default='new')
    # created_by = serializers.CharField(source='created_by.username')
    # assignee = UserSerializer()
    # created = serializers.DateTimeField()
    # updated = serializers.DateTimeField()
    class Meta:
        model = Card
        fields = ['id', 'title', 'content', 'status', 'assignee', 'created_by', 'created', 'updated']

    def validate_creator(self, value):
        if User.is_manager:
            raise serializers.ValidationError('Only users can create cards')
        return value

    class StatusSerializer(serializers.ModelSerializer):

        class Meta:
            model = Card
            fields = ['id', 'title', 'content', 'status', 'assignee', 'created_by', 'created', 'updated']




# urlpatterns = [
#     url(r'^', include(router.urls)),
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]
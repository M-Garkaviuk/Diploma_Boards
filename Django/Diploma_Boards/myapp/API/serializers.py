from myapp.models import Card, User
from rest_framework import routers, serializers, viewsets


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']



class CardViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id','title', 'content', 'status', 'assignee', 'created_by']

    # def validate_created_by(self, value):
    #     print(value)
    #     if User.is_manager:
    #         raise serializers.ValidationError('Only users can create cards')
    #     return value

    # def create(self, validated_data):
    #
    #     validated_data.pop("user")
    #     return super().create(validated_data=validated_data)




    class CardStatusSerializer(serializers.ModelSerializer):

        class Meta:
            model = Card
            fields = ['title', 'content', 'status', 'assignee']




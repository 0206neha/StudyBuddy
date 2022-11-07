#serialzers are classes that take a certain a model or object that we wantt to serialize.it take our python object and convert into json or javascript object.

from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer):
    class Meta:
        model=Room
        fields='__all__'

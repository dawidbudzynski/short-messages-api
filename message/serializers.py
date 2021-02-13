from rest_framework import serializers

from message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for message objects, doesn't allow to display/modify 'view' field"""

    class Meta:
        model = Message
        fields = ('id', 'content',)
        read_only_fields = ('id', 'views',)


class MessageDetailSerializer(serializers.ModelSerializer):
    """Serializer for message objects, allows to display 'view' field"""

    class Meta:
        model = Message
        fields = ('id', 'content', 'views',)
        read_only_fields = ('id',)

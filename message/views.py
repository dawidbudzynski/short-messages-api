from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from message import serializers
from message.models import Message


class ListMessageView(generics.ListAPIView):
    """List all messages"""
    serializer_class = serializers.MessageDetailSerializer
    queryset = Message.objects.order_by('id')


class CreateMessageView(generics.CreateAPIView):
    """Create new message"""
    serializer_class = serializers.MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class DetailsMessageView(generics.RetrieveAPIView):
    """Displays selected message"""
    serializer_class = serializers.MessageDetailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Message.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # increase view counter by 1 every time message is displayed
        previous_views_count = instance.views
        instance.views = previous_views_count + 1
        instance.save()

        return Response(serializer.data)


class UpdateMessageView(generics.UpdateAPIView):
    """Updates selected message"""
    serializer_class = serializers.MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Message.objects.all()

    def perform_update(self, serializer):
        """Reset view counter every time message is updated"""
        serializer.save(views=0)


class DeleteMessageView(generics.DestroyAPIView):
    """Deletes selected message"""
    serializer_class = serializers.MessageSerializer
    queryset = Message.objects.all()

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from message.models import Message
from message.serializers import MessageDetailSerializer

MESSAGES_LIST_URL = reverse('message:list')
MESSAGES_CREATE_URL = reverse('message:create')
MESSAGES_UPDATE_URL = reverse('message:update', args=[1])
MESSAGES_DELETE_URL = reverse('message:delete', args=[1])


class PublicMessagesApiTests(TestCase):
    """Test publicly available message API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_login_required(self):
        """Test that login is required for retrieving messages"""
        res = self.client.post(MESSAGES_CREATE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_login_required(self):
        """Test that login is required for updating messages"""
        res = self.client.put(MESSAGES_UPDATE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_login_required(self):
        """Test that login is required for deleting messages"""
        res = self.client.delete(MESSAGES_DELETE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMessagesApiTests(TestCase):
    """Test the authorized user messages API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'testuser@mail.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_messages(self):
        """Test retrieving messages"""
        Message.objects.create(user=self.user, content='Message 1')
        Message.objects.create(user=self.user, content='Message 2')

        res = self.client.get(MESSAGES_LIST_URL)
        messages = Message.objects.all().order_by('id')
        serializer = MessageDetailSerializer(messages, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_message_successful(self):
        """Test creating a new message"""
        payload = {'content': 'Message 4'}
        self.client.post(MESSAGES_CREATE_URL, payload)

        exists = Message.objects.filter(
            user=self.user,
            content=payload['content']
        ).exists()
        self.assertTrue(exists)

    def test_create_message_invalid(self):
        """Test creating a new message with invalid payload"""
        payload = {'content': ''}
        res = self.client.post(MESSAGES_CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

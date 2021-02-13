from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from message.models import Message
from message.serializers import MessageDetailSerializer

MESSAGES_LIST_URL = reverse('message:list')
MESSAGES_CREATE_URL = reverse('message:create')


class PublicMessagesApiTests(TestCase):
    """Test publicly available message API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'testuser@mail.com',
            'password123'
        )
        self.client = APIClient()

    def test_create_login_required(self):
        """Test that login is required for retrieving messages"""
        res = self.client.post(MESSAGES_CREATE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_login_required(self):
        """Test that login is required for updating messages"""
        res = self.client.put(reverse('message:update', args=[1]))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_login_required(self):
        """Test that login is required for deleting messages"""

        # creating message which can be later deleted, and logging out
        self.client.force_authenticate(self.user)
        new_message = Message.objects.create(user=self.user, content='Message 1')
        self.client.logout()

        message_delete_url = reverse('message:delete', args=[new_message.id])
        res = self.client.delete(message_delete_url)
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

    def test_details_view_counter(self):
        """Test details and view counter"""
        payload_1 = {'content': 'Message 5'}
        self.client.post(MESSAGES_CREATE_URL, payload_1)
        selected_message = Message.objects.get(
            user=self.user,
            content=payload_1['content']
        )
        self.assertEqual(selected_message.views, 0)

        self.client.get(reverse('message:details', args=[selected_message.id]))
        self.assertEqual(Message.objects.get(id=selected_message.id).views, 1)

        self.client.get(reverse('message:details', args=[selected_message.id]))
        self.assertEqual(Message.objects.get(id=selected_message.id).views, 2)

    def test_update_message_successful(self):
        """Test updating message and reseting views counter"""
        payload_1 = {'content': 'Message 5'}
        self.client.post(MESSAGES_CREATE_URL, payload_1)
        selected_message = Message.objects.get(
            user=self.user,
            content=payload_1['content']
        )

        # setting views counter to 10
        selected_message.views = 10
        selected_message.save()
        self.assertEqual(selected_message.views, 10)

        payload_2 = {'content': 'Message New'}
        res = self.client.put(
            reverse('message:update', args=[selected_message.id]),
            payload_2
        )
        updated_message = Message.objects.get(id=selected_message.id)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_message.content, payload_2['content'])
        self.assertEqual(updated_message.views, 0)

    def test_delete_message_successful(self):
        """Test deleting message"""

        # creating message which can be later deleted, and logging out
        new_message = Message.objects.create(user=self.user, content='Message 1')

        message_delete_url = reverse('message:delete', args=[new_message.id])
        res = self.client.delete(message_delete_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

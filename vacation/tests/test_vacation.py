from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Vacation
from node.models import Node, NodeConnection

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from model_bakery import baker


class VacationTest(APITestCase):
    def setUp(self):
        self.user = baker.make(get_user_model(), role='E')
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        self.node1 = baker.make(Node)
        self.node2 = baker.make(Node)
        self.node_connection = baker.make(NodeConnection, from_node=self.node1, to_node=self.node2)

    def test_create_vacation(self):
        url = reverse('vacation:create')
        data = {
            'user': self.user.id,
            'from_date': "2024-01-29T07:22:33.432520Z",
            'to_date': "2025-01-29T07:22:33.432530Z",
            'description': 'test',
            'status': 'P',
        }

        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertGreaterEqual(Vacation.objects.all().count(), 1)

    def test_list_vacations(self):
        vacations = baker.make(Vacation, _quantity=10)
        url = reverse('vacation:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_retrieve_vacation(self):
        vacation = baker.make(Vacation, user=self.user)
        url = reverse('vacation:update-destroy-retrieve', kwargs={'pk': vacation.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(Vacation.objects.all().count(), 1)

    def test_update_vacation(self):
        vacation = baker.make(Vacation, user=self.user)
        url = reverse('vacation:update-destroy-retrieve', kwargs={'pk': vacation.id})
        data = {
            'from_date': "2024-01-29T07:22:33.432520Z",
            'description': 'Updated description',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_vacation(self):
        vacation = baker.make(Vacation, user=self.user)
        url = reverse('vacation:update-destroy-retrieve', kwargs={'pk': vacation.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
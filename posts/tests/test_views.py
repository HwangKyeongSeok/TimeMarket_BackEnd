# tests/test_time_posts.py
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from posts.models import TimePost

User = get_user_model()

class TimePostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(nickname='testuser222', email="testuser2", password='testpas22s')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.post_data = {
            "title": "Test Time Sale",
            "description": "I will help you move for 1 hour",
            "type": "sale",
            "latitude": 37.5,
            "longitude": 127.0,
        }

        self.time_post = TimePost.objects.create(
            user=self.user,
            title="Test Post",
            description="Help with cleaning",
            type="sale",
            latitude=37.5,
            longitude=127.0,
        )

    def test_create_time_post(self):
        url = reverse('timepost-create')
        response = self.client.post(url, self.post_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert TimePost.objects.count() == 2

    def test_list_time_posts_with_gps(self):
        url = reverse('timepost-board') + '?lat=37.5&lng=127.0&type=sale'
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_get_time_post_detail(self):
        url = reverse('timepost-detail', args=[self.time_post.id])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == self.time_post.title

    def test_update_time_post(self):
        url = reverse('timepost-detail', args=[self.time_post.id])
        response = self.client.patch(url, {'title': 'Updated Title'}, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.time_post.refresh_from_db()
        assert self.time_post.title == 'Updated Title'

    def test_delete_time_post(self):
        url = reverse('timepost-detail', args=[self.time_post.id])
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert TimePost.objects.count() == 0

    def test_list_time_posts_board_mode(self):
        url = reverse('timepost-board')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

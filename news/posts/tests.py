from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Comment, Post, Upvote

User = get_user_model()


class PostTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(email='test1@mail.com', username='test_user1', password='Test1234')
        self.user2 = User.objects.create_user(email='test2@mail.com', username='test_user2', password='Test1234')
        self.post1 = Post.objects.create(author=self.user1, title='post1')
        self.post2 = Post.objects.create(author=self.user1, title='post2')
        self.comment1 = Comment.objects.create(post=self.post1, content='test content', author=self.user2)
        self.comment2 = Comment.objects.create(post=self.post2, content='test content', author=self.user1)

    def test_posts_list(self):
        url = reverse('posts_list_url')
        response = self.client.get(url)
        posts = Post.objects.all()
        db_post_titles = []
        response_post_titles = []
        for post in posts:
            db_post_titles.append(post.title)
        for post in response.data:
            response_post_titles.append(post.get('title'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(db_post_titles, response_post_titles)

    def test_post_create(self):
        url = reverse('posts_list_url')
        data = {'title': 'new title'}
        self.client.force_authenticate(self.user1)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.all().first()
        self.assertEqual(response.data.get('id'), post.id)
        self.assertEqual(response.data.get('author_name'), self.user1.username)

    def test_retrieve_post(self):
        url = reverse('post_detail_url', kwargs={'id': self.post1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), self.post1.title)

    def test_update_post(self):
        url = reverse('post_detail_url', kwargs={'id': self.post1.id})
        data = {'title': 'brand new title'}
        self.client.force_login(self.user1)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'brand new title')

    def test_update_post_permission(self):
        url = reverse('post_detail_url', kwargs={'id': self.post2.id})
        data = {'title': 'brand new title'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post(self):
        url = reverse('post_detail_url', kwargs={'id': self.post2.id})
        self.client.force_login(self.user1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_permission(self):
        url = reverse('post_detail_url', kwargs={'id': self.post1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_comments(self):
        url = reverse('comments_list_url', kwargs={'post_id': self.post1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment_ids = []
        for comment in response.data:
            comment_ids.append(comment.get('id'))
        self.assertEqual(comment_ids, [self.comment1.id, ])

    def test_create_comment(self):
        url = reverse('comments_list_url', kwargs={'post_id': self.post1.id})
        data = {'content': 'new comment'}
        self.client.force_login(self.user1)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_comment(self):
        url = reverse('comment_detail_url', kwargs={'post_id': self.post1.id, 'id': self.comment1.id})
        self.client.force_login(self.user2)
        data = {'content': 'test post'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('content'), 'test post')

    def test_update_comment_for_post_author(self):
        url = reverse('comment_detail_url', kwargs={'post_id': self.post1.id, 'id': self.comment1.id})
        self.client.force_login(self.user1)
        data = {'content': 'blah blah blah'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('content'), 'blah blah blah')

    def test_delete_comment(self):
        url = reverse('comment_detail_url', kwargs={'post_id': self.post1.id, 'id': self.comment1.id})
        self.client.force_login(self.user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_upvote_post(self):
        url = reverse('upvotes_url', kwargs={'post_id': self.post1.id})
        self.client.force_login(self.user2)
        response = self.client.post(url)
        self.post1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'You have upvoted the post')
        self.assertEqual(self.post1.upvotes_amount, 1)
        response = self.client.post(url)
        self.post1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post1.upvotes_amount, 1)
        self.assertEqual(response.data, 'You have already upvoted this post today')

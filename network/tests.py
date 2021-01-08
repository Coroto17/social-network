from django.test import TestCase, Client
from .models import Post, User
from django.urls import reverse

# Create your tests here.
class PostTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        # Create Users
        cls.u1 = User.objects.create(
            username="coroto", email="coroto@example.com", password="123456"
        )
        cls.u2 = User.objects.create(
            username="alice17", email="alice@example.com", password="123456"
        )
        # Create Posts
        cls.p1 = Post.objects.create(content="Test Post1", author=cls.u1)
        cls.p2 = Post.objects.create(content="Test Post2", author=cls.u2)
    
    def test_users_count(self) -> None:
        """Tests the number of dummy users created"""
        users = User.objects.all()
        self.assertEqual(users.count(), 2)

    def test_posts_count(self):
        """Tests the number of dummy posts created"""
        posts = Post.objects.all()
        self.assertEqual(posts.count(), 2)
    
    def test_post_author(self):
        """Tests the author of the post"""
        user = self.u1
        post = self.p1
        self.assertEqual(post.author, user)

    def test_valid_post(self):
        """Check that a post is valid"""
        post = Post.objects.first()
        self.assertEqual(post.is_valid_post(0), True)

class ClientTestCase(TestCase):

    def setUp(self):
        # Create Users
        u1 = User.objects.create_user(
            username="coroto", email="coroto@example.com", password="123456"
        )
        u2 = User.objects.create_user(
            username="alice17", email="alice@example.com", password="123456"
        )
        # Create Posts
        p1 = Post.objects.create(content="Test Post1", author=u1)
        p2 = Post.objects.create(content="Test Post2", author=u2)
    
    def test_index(self) -> None:
        """ test that posts appears on index"""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(isinstance(response.context["page_obj"][1], Post), True)

    def test_login(self):
        """test login of a given user"""
        client = Client()
        user = User.objects.get(username="coroto")
        credentials = {
            "username": user.username,
            "password": "123456"
        }
        response = client.post("/login", credentials)
        self.assertEqual(response.status_code, 302, msg="It didn't redirect")
        self.assertEqual(client.session.get("_auth_user_id"), str(user.id))
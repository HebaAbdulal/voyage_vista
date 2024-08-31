from django.test import TestCase, Client
from django.urls import reverse
from voyagevista.models import Post



class TestViews(TestCase):
    """
    Unit tests for views in the VoyageVista app
    """
    def setUp(self):
        """
        Create test users and posts.
        """
        self.user = User.objects.create_user(username='testuser', password='testpass')
        logged_in = self.client.login(username='testuser', password='testpass')
        self.assertTrue(logged_in, "Login failed in setUp method")
        
        self.category = Category.objects.create(name='Test Category')
        
        self.post = Post.objects.create(
            title="test title",
            slug="test-title",
            author=self.user,
            content="Content of test post",
            category=self.category,
            status=1
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        """
        Test the correct template is used for the home page.
        """
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, template_name='index.html')

    def test_posts_passed_into_template(self):
        """
        Test that the blog posts are passed into the blog template.
        """
        response = self.client.get(reverse('home'))
        posts = Post.objects.all()
        self.assertEqual(len(response.context['page_obj']), len(posts))
        self.assertQuerySetEqual(
            response.context['page_obj'],
            posts,
            transform=lambda x: x
        )

    def test_post_detail(self):
        """
        Test the post detail page.
        """
        post = self.post  # Use the post created in setUp
        response = self.client.get(reverse('post_detail', args=[post.slug]))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_template(self):
        """
        Test the correct template is used for the post detail page.
        """
        post = Post.objects.first()  # Get the first post
        response = self.client.get(reverse('post_detail', args=[post.slug]))
        self.assertTemplateUsed(response, template_name='post_detail.html')

    def test_add_post(self):
        """
        Test to see if user logged in can access add post page.
        """
        self.client.login(username='testuser', password='12345')  # Log in the user
        response = self.client.get(reverse('add_post'))
        self.assertEqual(response.status_code, 200)

    def test_add_post_template(self):
        """
        Test the correct template is used for the add post page.
        """
        self.client.login(username='testuser', password='12345')  # Log in the user
        response = self.client.get(reverse('add_post'))
        self.assertEqual(response.status_code, 200)  # Ensure we get a 200 status
        self.assertTemplateUsed(response, template_name='add_post.html')  # Check for the correct template

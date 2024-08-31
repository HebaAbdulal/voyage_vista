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

    def test_logged_out_user_redirected_from_add_post(self):
        """
        test to ensure logged out user is redirected
        and can not access add blog post page
        """
        self.client.logout()
        response = self.client.get(reverse('add_post'))
        self.assertEqual(response.status_code, 302)

    def test_adding_post(self):
        """
        Test that a logged-in user can add a post.
        """
        initial_count = Post.objects.count()
        self.client.login(username='testuser', password='12345')
        
        # Data for new post
        data = {
            'title': 'Page Submitted Post',
            'slug': 'page-submitted-post',
            'content': 'Page submitted post content',
            'status': 1
        }
        
        response = self.client.post(reverse('add_post'), data)
        
        # Check if post count has increased by 1
        self.assertEqual(Post.objects.count(), initial_count + 1)
        
        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'success')
        
        # Check for redirect
        self.assertEqual(response.status_code, 302)


class TestEditPostView(TestCase):
    """
    Unit tests for the EditPostView in the VoyageVista app.
    """
    def setUp(self):
        """
        Create test users and posts.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category')  # Create a test category

        self.post = Post.objects.create(
            title="test title",
            slug="test-title",
            author=self.user,
            content="Content of test post",
            category=self.category,  # Assign the created category
            status=1
        )
    
    def test_edit_post_view_get(self):
        """
        Test GET request for the edit post view.
        """
        self.client.login(username='testuser', password='12345')  # Log in the user
        response = self.client.get(reverse('edit_post', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_post.html')
        self.assertContains(response, 'name="title"')  # Check if the form has a title field
        self.assertContains(response, 'name="content"')  # Check if the form has a content field

    def test_edit_post_view_post_valid(self):
        """
        Test POST request with valid data to edit a post.
        """
        self.client.login(username='testuser', password='12345')  # Log in the user
        data = {
            'title': 'Updated Title',
            'category': self.category.id,
            'content': 'Updated content',
        }
        response = self.client.post(reverse('edit_post', kwargs={'slug': self.post.slug}), data)
        self.assertEqual(response.status_code, 302)

        # Refresh the post from the database and verify changes
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
        self.assertEqual(self.post.content, 'Updated content')
        self.assertFalse(self.post.approved)
        self.assertEqual(self.post.status, 0)

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, 'Post updated successfully and is now awaiting approval.')

    def test_edit_post_view_post_invalid(self):
        """
        Test POST request with invalid data to ensure form errors are handled.
        """
        self.client.login(username='testuser', password='12345')  # Log in the user
        data = {
            'title': '',  # Invalid title
            'category': self.category.id,
            'content': 'Content without a valid title',
        }
        response = self.client.post(reverse('edit_post', kwargs={'slug': self.post.slug}), data)
        self.assertEqual(response.status_code, 200)  # Should stay on the same page

        # Check for form errors in the response
        self.assertContains(response, 'This field is required.')

        # Check if the post has not been updated
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'test title')
        self.assertEqual(self.post.content, 'Content of test post')

    def test_edit_post_view_no_permission(self):
        """
        Test to ensure users who are not the author cannot edit the post.
        """
        # Create another user
        other_user = User.objects.create_user(username='otheruser', password='12345')

        # Log in as the other user
        self.client.login(username='otheruser', password='12345')

        data = {
            'title': 'Malicious Update',
            'category': self.category.id,
            'content': 'Content by unauthorized user',
        }
        response = self.client.post(reverse('edit_post', kwargs={'slug': self.post.slug}), data)
        self.assertEqual(response.status_code, 302)

        # Check if redirected to the post detail
        self.assertRedirects(response, reverse('post_detail', kwargs={'slug': self.post.slug}))

        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, 'You do not have permission to edit this post.')

        # Verify the post has not been changed
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'test title')
        self.assertEqual(self.post.content, 'Content of test post')


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


class TestDeletePostView(TestCase):

    def setUp(self):
        """
        Create test users and posts.
        """
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Log in the user and assert login success
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

    def test_delete_post(self):
        """
        Test that a post is deleted successfully by the author.
        """
        post = Post.objects.get(title='test title')
        self.assertEqual(Post.objects.count(), 1)

        # Attempt to delete the post
        response = self.client.post(reverse('delete_post', kwargs={'slug': post.slug}))

        # Check for redirect to home page after successful deletion
        self.assertRedirects(response, reverse('home'))

        # Check if post is deleted
        self.assertEqual(Post.objects.count(), 0)

        # Check if success message is in messages
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'success')
        self.assertIn('Post deleted successfully.', messages[0].message)

    def test_logged_out_user_delete_blog_post(self):
        """
        Test if the user is logged out
        that they can't delete a post
        by sending the request to the url
        """
        post = Post.objects.get(title='test title')
        self.assertEqual(Post.objects.count(), 1)
        self.client.logout()
        response = self.client.post(reverse('delete_post', kwargs={'slug': post.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)


class MyLikesViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        logged_in = self.client.login(username='testuser', password='testpass')
        self.assertTrue(logged_in, "Login failed in setUp method")
        
        self.category = Category.objects.create(name='Test Category')
        
        self.posts = [
            Post.objects.create(
                title=f"Post {i}",
                slug=f"post-{i}",
                author=self.user,
                content=f"Content of test post {i}",
                category=self.category,
                status=1
            ) for i in range(1, 10)  # Create 9 posts
        ]
        
        self.user.blog_likes.set(self.posts[:5])  # The user likes the first 5 posts

    def test_my_likes_view(self):
        """
        Test that the MyLikesView displays liked posts correctly.
        """
        url = reverse('my_likes')
        response = self.client.get(url)
        
        # Check for successful response
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct template is used
        self.assertTemplateUsed(response, 'my_likes.html')
        
        # Check that the context contains liked posts
        liked_posts = response.context['liked_posts']
        self.assertTrue(isinstance(liked_posts, Page))
        self.assertEqual(len(liked_posts.object_list), 4)  # Check if the default page size (4) is correct

        # Check pagination
        self.assertEqual(response.context['page_obj'].number, 1)

        liked_post_titles = [post.title for post in liked_posts.object_list]
        expected_titles = [post.title for post in self.posts[4:0:-1]]  # Fetch the first 4 posts and reverse
        
        for title in expected_titles:
            self.assertIn(title, liked_post_titles)


    def test_my_likes_view_pagination(self):
        """
        Test pagination of liked posts in MyLikesView.
        """
        url = reverse('my_likes') + '?page=2'
        response = self.client.get(url)
        
        # Check for successful response
        self.assertEqual(response.status_code, 200)
        
        # Check pagination to see if it handles pages correctly
        liked_posts = response.context['liked_posts']
        self.assertTrue(isinstance(liked_posts, Page))
        self.assertEqual(liked_posts.number, 2)
        
        # Verify the posts on page 2
        self.assertEqual(len(liked_posts.object_list), 1)
        self.assertEqual(liked_posts.object_list[0].title, 'Post 1')


class CommentEditTest(TestCase):
    """
    Test case for editing comments in the CommentEdit view.
    """
    def setUp(self):
        """
        Set up the test environment by creating a user, a post, and a comment.
        """
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post.',
            author=self.user,
            created_on=timezone.now(),
            status=1
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body='This is a test comment.',
            approved=True
        )
        self.url = reverse('edit_comment', kwargs={'slug': self.post.slug, 'pk': self.comment.pk})
    
    def test_get_edit_form_valid_user(self):
        """
        Test that a logged-in user with permission can access the edit comment form.

        This test logs in a user who is the author of the comment and verifies that
        the response status is 200 and the correct template and content are used.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html')
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'This is a test comment.')

    def test_get_edit_form_valid_user(self):
        """
        Test that a user without permission is redirected when attempting to access
        the edit comment form.

        This test logs in a user who is not the author of the comment and verifies
        that the response is a redirect and the user is redirected to the post detail page.
        """
        self.client.login(username='testuser', password='password')

        # Generate unique title and slug
        unique_title = f"Test Post {uuid.uuid4()}"
        unique_slug = slugify(unique_title)
        
        # Create a post and comment
        post = Post.objects.create(title=unique_title, content='Test Content', author=self.user, slug=unique_slug, status=1)
        comment = Comment.objects.create(body='Test Comment', post=post, author=self.user)
        url = reverse('edit_comment', kwargs={'slug': post.slug, 'pk': comment.pk})
        
        # Access the edit form with the valid user
        response = self.client.get(url)
        
        # Check the response
        self.assertEqual(response.status_code, 200)


class CommentDeleteViewTest(TestCase):
    """
    Test suite for the CommentDeleteView.
    """
    
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', password='testpassword')
        
        # Create a post
        self.post = Post.objects.create(title='Test Post', content='This is a test post', author=self.user, status=1, slug='test-post')
        
        # Create a comment
        self.comment = Comment.objects.create(post=self.post, author=self.user, content='This is a test comment', approved=True)

    def test_get_delete_comment_form_valid_user(self):
        """
        Test that the comment is successfully deleted by the author.
        """
        # Log in as the author of the comment
        self.client.login(username='testuser', password='testpassword')
        
        # Send GET request to delete the comment
        response = self.client.get(reverse('delete_comment', kwargs={'slug': self.post.slug, 'pk': self.comment.pk}))
        
        # Assert that the user is redirected after deletion
        self.assertEqual(response.status_code, 302)
        
        # Follow the redirect
        response = self.client.get(response.url, follow=True)
        
        # Check that the success message is displayed
        self.assertContains(response, "Comment Deleted Successfully")
        
        # Assert that the comment is deleted
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=self.comment.pk)

    def test_get_delete_comment_form_invalid_user(self):
        """
        Test that the comment cannot be deleted by someone other than the author.
        """
        # Log in as a different user
        self.client.login(username='otheruser', password='testpassword')
        
        # Send GET request to delete the comment
        response = self.client.get(reverse('delete_comment', kwargs={'slug': self.post.slug, 'pk': self.comment.pk}))
        
        # Assert that the user is redirected
        self.assertEqual(response.status_code, 302)
        
        # Follow the redirect
        response = self.client.get(response.url, follow=True)
        
        # Check that the error message is displayed
        self.assertContains(response, 'You do not have permission to delete this comment.')
        
        # Assert that the comment is not deleted
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_get_delete_comment_form_unauthenticated_user(self):
        """
        Test that an unauthenticated user cannot delete a comment.
        """
        # Send GET request to delete the comment without logging in
        response = self.client.get(reverse('delete_comment', kwargs={'slug': self.post.slug, 'pk': self.comment.pk}))
        
        # Assert that the user is redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
        
        # Assert that the comment is not deleted
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())


class PostBookmarkViewTest(TestCase):
    """
    Test suite for the PostBookmark view.
    """

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create a post
        self.post = Post.objects.create(
            title='Test Post', 
            content='This is a test post content.', 
            author=self.user, 
            status=1, 
            slug='test-post'
        )

    def test_post_bookmark_view_status_code(self):
        """
        Test that the bookmark view returns a 200 status code after bookmarking.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('post_bookmark', kwargs={'slug': self.post.slug}))
        
        # Assert the response is a redirect (302)
        self.assertEqual(response.status_code, 302)

        # Follow the redirect to the post detail page
        response = self.client.get(reverse('post_detail', kwargs={'slug': self.post.slug}))

        # Assert that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Post bookmarked.")
        
        # Check that the post is actually bookmarked by the user
        self.assertTrue(self.post.saves.filter(id=self.user.id).exists())


class RatePostViewTest(TestCase):
    def setUp(self):
        # Create a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')

        # Create a test post with the logged-in user as the author
        self.post = Post.objects.create(
            title='Test Post', 
            slug='test-post', 
            content='Test Content', 
            author=self.user
        )

    def test_rate_post_successful(self):
        url = reverse('rate_post', kwargs={'post_slug': self.post.slug})
        data = {'rating': 4}
        response = self.client.post(url, data, content_type='application/json')

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the expected success message
        self.assertEqual(response.json()['success'], True)

        # Check that the average rating is calculated correctly
        average_rating = response.json()['average_rating']
        self.assertEqual(average_rating, 4.0)

        # Verify that the rating has been saved in the database
        rating = Rating.objects.get(user=self.user, post=self.post)
        self.assertEqual(rating.rating, 4)



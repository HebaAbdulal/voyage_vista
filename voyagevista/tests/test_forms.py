from unittest.mock import patch
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from voyagevista.models import Post, Category, Comment, Rating
from voyagevista.forms import PostForm, CommentForm, RatingForm, ContactForm
from django.contrib.auth.models import User


class PostFormTest(TestCase):
    def setUp(self):
        # Create a dummy user
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create categories
        self.category1 = Category.objects.create(name='Destinations', slug='destinations')
        self.category2 = Category.objects.create(name='Travel Tips', slug='travel-tips')

        # Setup valid test data including author
        self.valid_data = {
            'title': 'Test Post',
            'content': 'This is a test content.',
            'excerpt': 'This is a test excerpt.',
            'category': self.category1.id,  # Use category ID
        }
        
        # Create a small dummy image for testing
        self.image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

    @patch('cloudinary.uploader.upload', return_value={
        'url': 'http://example.com/image.jpg',
        'public_id': 'test_public_id',
        'version': 1234567890,
        'signature': 'abcdef1234567890',
        'width': 800,
        'height': 600,
        'format': 'jpg',
        'resource_type': 'image',
        'created_at': '2023-08-01T00:00:00Z',
        'secure_url': 'https://example.com/image.jpg',
        'type': 'upload'  # Ensure 'type' is included
    })
    def test_valid_form(self, mock_upload):
        form = PostForm(data=self.valid_data, files={'featured_image': self.image_file})
        self.assertTrue(form.is_valid())
        
        # Assign the author after form validation
        post = form.save(commit=False)
        post.author = self.user  # Assign the author
        post.save()

        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test content.')
        self.assertEqual(post.excerpt, 'This is a test excerpt.')
        self.assertEqual(post.category, self.category1)
        self.assertFalse(post.approved)

    def test_invalid_form(self):
        # Missing title
        form = PostForm(data={
            'content': 'This is a test content.',
            'excerpt': 'This is a test excerpt.',
            'category': self.category1.id,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    @patch('cloudinary.uploader.upload', return_value={
        'url': 'http://example.com/image.jpg',
        'public_id': 'test_public_id',
        'version': 1234567890,
        'signature': 'abcdef1234567890',
        'width': 800,
        'height': 600,
        'format': 'jpg',
        'resource_type': 'image',
        'created_at': '2023-08-01T00:00:00Z',
        'secure_url': 'https://example.com/image.jpg',
        'type': 'upload'
    })
    def test_save_method(self, mock_upload):
        form = PostForm(data=self.valid_data, files={'featured_image': self.image_file})
        if not form.is_valid():
            self.fail("Form is not valid")
        
        post = form.save(commit=False)
        post.author = self.user  # Assign the author
        post.save()

        self.assertFalse(post.approved)
        self.assertTrue(Post.objects.filter(id=post.id).exists())


class CommentFormTest(TestCase):
    def setUp(self):
        # Create a dummy user
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create a category and a post for the comment to be associated with
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test content.',
            excerpt='This is a test excerpt.',
            author=self.user,
            approved=True,
            category=self.category
        )

        # Setup valid test data
        self.valid_data = {
            'body': 'This is a test comment.',
        }
    
    def test_valid_form(self):
        form = CommentForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

        # Check if the form saves the data correctly
        comment = form.save(commit=False)
        comment.post = self.post
        comment.user = self.user
        comment.save()

        self.assertEqual(comment.body, 'This is a test comment.')
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.user, self.user)

    
    def test_invalid_form(self):
        # Missing 'body'
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors)

        # Validate the error messages if required
        self.assertEqual(form.errors['body'], ['This field is required.'])


class RatingFormTest(TestCase):
    def setUp(self):
        # Create a dummy user
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create a category
        self.category = Category.objects.create(name='Destinations', slug='destinations')

        # Create a post for the rating to be associated with
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test content.',
            excerpt='This is a test excerpt.',
            author=self.user,
            approved=True,
            category=self.category
        )

        # Setup valid and invalid test data
        self.valid_data = {
            'rating': 5,
        }
        self.invalid_data = {
            'rating': 11,
        }
    
    def test_valid_form(self):
        form = RatingForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

        # Check if the form saves the data correctly
        rating = form.save(commit=False)
        rating.post = self.post
        rating.user = self.user
        rating.save()

        self.assertEqual(rating.rating, 5)
        self.assertTrue(Rating.objects.filter(id=rating.id).exists())

    def test_invalid_form(self):
        form = RatingForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

        # Validate the error messages if required
        self.assertEqual(form.errors['rating'], ['Rating must be between 1 and 10.'])


class ContactFormTest(TestCase):
    def setUp(self):
        # Set up valid and invalid test data
        self.valid_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'message': 'This is a test message.',
        }
        self.invalid_data = {
            'name': '',  # Empty name
            'email': 'invalid-email',  # Invalid email format
            'message': '',  # Empty message
        }

    def test_valid_form(self):
        form = ContactForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = ContactForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        
        # Check if the errors are correctly identified
        self.assertIn('name', form.errors)  # Should fail due to empty name
        self.assertIn('email', form.errors)  # Should fail due to invalid email format
        self.assertIn('message', form.errors)  # Should fail due to empty message
        
        # Validate the error messages if required
        self.assertEqual(form.errors['name'], ['This field is required.'])
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])
        self.assertEqual(form.errors['message'], ['This field is required.'])

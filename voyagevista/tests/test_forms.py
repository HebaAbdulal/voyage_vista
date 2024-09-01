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
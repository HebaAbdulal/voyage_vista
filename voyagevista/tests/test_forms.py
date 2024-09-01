from unittest.mock import patch
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from voyagevista.models import Post, Category, Comment, Rating
from voyagevista.forms import PostForm, CommentForm, RatingForm, ContactForm
from django.contrib.auth.models import User
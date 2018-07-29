from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):
	name = models.CharField(max_length = 255)
	description = models.CharField(max_length = 255)

class Topic(models.Model):
	subject = models.CharField(max_length = 255)
	last_update = models.DateTimeField(auto_now_add = True)
	board = models.ForeignKey(Board, on_delete = models.CASCADE, related_name = 'topics')
	starter = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'topics')

class Post(models.Model):
	message = models.CharField(max_length = 4000)
	topic = models.ForeignKey(Topic, on_delete = models.CASCADE, related_name = 'posts')
	created_at = models.DateTimeField(auto_now_add = True, null = True)
	updated_at = models.DateTimeField(null = True)
	created_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'posts')
	updated_by = models.ForeignKey(User, on_delete = models.CASCADE, null = True, related_name = '+')
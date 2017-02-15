from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
	"""learing subjects of users"""
	text = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User)

	def __str__(self):
		"""return the string format of the model"""
		return self.text


class Entry(models.Model):
	"""specific knowledge of a subject"""
	topic = models.ForeignKey(Topic)
	text = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'entries'

	def __str__(self):
		"""return the string format of the model"""
		return self.text[:50] + "..."
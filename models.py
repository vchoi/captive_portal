from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class DeviceAuthorization(models.Model):
	mac_address = models.CharField(max_length="17")
	ip_address = models.GenericIPAddressField()
	created = models.DateTimeField(
		auto_now_add=True,
		help_text='create time',
		)
	last_modified = models.DateTimeField(
		auto_now=True,
		help_text='last modification time',
		)
	expires = models.DateTimeField(
		default=timezone.now()+timedelta(days=1),
		help_text='when this authorization should be discarded',
		)


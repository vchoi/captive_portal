from django.db import models
from django.utils import timezone
from django.conf import settings
import datetime
import pytz

# Create your models here.
_tz = pytz.timezone(settings.TIME_ZONE)
def _now():
	return datetime.datetime.now(_tz)

def _midnight():
	now = _now()
	return datetime.datetime(now.year, now.month, now.day, 23, 59, 59, tzinfo=_tz)

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
		default=_midnight,
		help_text='when this authorization should be discarded',
		)

	def __unicode__(self):
		return '<DeviceAuthorization:%i,%s,%s,%s,%s>' % (
			self.id,
			self.mac_address, self.ip_address, self.created,
			self.expires)

	@staticmethod
	def filter_not_expired():
                return DeviceAuthorization.objects.filter(expires__gt=_now())

	@staticmethod
	def filter_expired():
		return DeviceAuthorization.objects.filter(expires__lte=_now())


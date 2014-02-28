from django.core.management.base import BaseCommand, CommandError
from captive_portal.models import DeviceAuthorization

class Command(BaseCommand):
	args = ''
	help = 'List all DeviceAuthorizations'

	def handle(self, *args, **options):
		for da in DeviceAuthorization.objects.all():
			self.stdout.write(str(da))

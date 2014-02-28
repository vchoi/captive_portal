from django.core.management.base import BaseCommand, CommandError
from captive_portal.models import DeviceAuthorization
from captive_portal.util import Firewall

class Command(BaseCommand):
	args = ''
	help = 'Clear all DeviceAuthorizations'

	def handle(self, *args, **options):
		DeviceAuthorization.objects.all().delete()
		fw = Firewall()
		fw.reload_rules()
		

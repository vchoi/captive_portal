from django.core.management.base import BaseCommand, CommandError
from captive_portal.util import Firewall

class Command(BaseCommand):
	args = ''
	help = 'Reload firewall rules'

	def handle(self, *args, **options):
		fw = Firewall()
		fw.reload_rules()

		self.stdout.write('Successfully reloaded firewall rules')

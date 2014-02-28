from django.core.management.base import BaseCommand, CommandError
import logging
from captive_portal.util import Firewall
from captive_portal.models import DeviceAuthorization

class Command(BaseCommand):
	args = ''
	help = 'Check and remove expired authorizations'

	def handle(self, *args, **options):
		logging.info('check_authorizations')
		fw = Firewall()
		expired_authorizations = DeviceAuthorization.filter_expired()
		for da in expired_authorizations:
			logging.info('deleting %s' % da)
			try:
				fw.del_authorization(da)
			except:
				pass
			da.delete()

		#self.stdout.write('Successfully reloaded firewall rules')

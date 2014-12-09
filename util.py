from captive_portal.models import DeviceAuthorization
from django.conf import settings
import logging
import subprocess
import pytz
import datetime

class ArpCache:
	"""/proc/net/arp interface.
	self.cache format: [
		'IP address', 
		'HW type',
		'Flags',
		'HW address',
		'Mask',
		'Device']
	"""
	
	def __init__(self):
		self.update()
		
	def update(self):
		f = file('/proc/net/arp', 'r')
		output = [line.strip().split() for line in f.readlines()]
		f.close()
		self.cache = output[1:]

	def get_mac(self, ip=None):
		if type(ip) != type(''):
			raise ValueError('ip must be a string')
		ip = ip.strip()

		for entry in self.cache:
			if entry[0] == ip:
				return entry[3]

		raise KeyError('ip %s not in arp cache' % ip)

def time_now():
	tz=pytz.timezone(settings.TIME_ZONE)
	return datetime.datetime.now(tz)

def time_midnight():
	"""Returns a tz-aware datetime object for the end of this day"""
	now = time_now()
	return datetime.datetime(now.year, now.month, now.day, 23, 59, 59, tzinfo=tz)

_firewall_rules_template = """"""

class Firewall:
	"""firewall class to serve the captive portal"""

	def __init__(self):
		self.base_rules = settings.CAPTIVE_PORTAL['firewall_rules_template'] % settings.CAPTIVE_PORTAL
		self.authorization_rule_template = settings.CAPTIVE_PORTAL['authorization_rule_template']

               # load kernel modules
               modprobe = settings.CAPTIVE_PORTAL['modprobe']:
               for kernel_module in settings.CAPTIVE_PORTAL['kernel_modules']:
                       cmd += ("%s %s" % (modprobe, kernel_module))
                       self._run_cmd(cmd)

	def _run_cmd(self, cmd):
		try:
                        child = subprocess.check_call(cmd.split(), stderr=subprocess.PIPE)
                except subprocess.CalledProcessError:
                        logger = logging.getLogger()
                        logger.warning("error running %s" % cmd)

	def reload_rules(self):
		logger = logging.getLogger()
		logger.debug('loading firewall rules')
		try:
			child = subprocess.Popen(settings.CAPTIVE_PORTAL['iptables-restore'],
				stdin = subprocess.PIPE)
			child.stdin.write(self.base_rules)
			child.stdin.close()
			child.wait()
		except subprocess.CalledProcessError:
			logger.warning("error loading boilerplate rules")

	        now = time_now()
		valid_authorizations = DeviceAuthorization.objects.filter(expires__gt=now)
		for da in valid_authorizations:
			self.add_authorization(da)

	def add_authorization(self, device_authorization):
		logger = logging.getLogger()
                logger.debug('activating device authorization: %s' % device_authorization)

		cmd = settings.CAPTIVE_PORTAL['iptables']
		opts = ' -t mangle -A authorized ' + self.authorization_rule_template
		opts = opts % {'mac': device_authorization.mac_address,
				'ip': device_authorization.ip_address}
		cmd += opts
		self._run_cmd(cmd)


	def del_authorization(self, device_authorization):
		logger = logging.getLogger()
                logger.debug('removing device authorization: %s' % device_authorization)
		cmd = settings.CAPTIVE_PORTAL['iptables']
		opts = ' -t mangle -D authorized ' + self.authorization_rule_template
		opts = opts % {'mac': device_authorization.mac_address,
                                'ip': device_authorization.ip_address}
		cmd += opts
		self._run_cmd(cmd)


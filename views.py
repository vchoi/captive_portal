from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from captive_portal.models import DeviceAuthorization
from captive_portal.util import ArpCache, Firewall

def home(request):
	return redirect('/cp/splash', permanent=False)

def splash(request):
	context = {'key': 'value'}
	return render(request,'captive_portal/splash.html', context)

def splash_action(request):
	if not request.POST.has_key('accept'):
		return HttpResponseForbidden('Not authorized')

	# user accepted
	client_ip = request.META['REMOTE_ADDR']
	try:
		c = ArpCache()
		client_mac = c.get_mac(client_ip)
	except KeyError:
		client_mac=''

	auth = DeviceAuthorization(ip_address=client_ip, mac_address=client_mac)
	auth.save()

	fw = Firewall()
	fw.add_authorization(auth)

	context = {'device_authorization': auth}

	return render(request, 'captive_portal/splash_action.html', context)

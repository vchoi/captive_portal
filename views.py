from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from captive_portal.models import DeviceAuthorization

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
	auth = DeviceAuthorization(ip_address=client_ip)
	auth.save()

	context = {'device_authorization': auth}

	return render(request, 'captive_portal/splash_action.html', context)

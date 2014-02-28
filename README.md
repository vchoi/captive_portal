Django Captive Portal
==============

django captive portal.


My Notes
--------
* Create a django project: $ django-admin.py startproject mylanportal
* Download the Captive Portal app: $ cd mylanportal ; git clone https://github.com/vchoi/captive_portal.git
* Add captive_portal to INSTALLED_APPS
* Add CAPTIVE_PORTAL to settings.py (see SETTINGS)
* Copy captive_portal-check_authorizations to /etc/cron.d/
* echo 1 > /proc/sys/net/ipv4/ip_forward
* Get a working DHCP

Management Commands
-------------------

Management commands are run like this:
```
python manage.py management_command
```

Available commands:
* check_authorizations: check for expired device authorizations, delete them from firewall and database
* clear_authorizations: clear all device authorizations
* list_authorizations: list all device authorizations, valid or not
* reload_firewall: reload the firewall rules template and add any valid device authorizations

SETTINGS
--------

Add this to your project's settings.py

```python
CAPTIVE_PORTAL = {
    'LAN_IF': 'eth0',
    'LAN_IP': '10.0.0.1',
    'WAN_IF': 'eth1',
    'WAN_IP': '192.0.2.1',
    'iptables-restore': '/sbin/iptables-restore',
    'iptables': '/sbin/iptables',
    'authorization_rule_template': '-s %(ip)s -m mac --mac-source %(mac)s -j MARK --set-mark 1',
    'firewall_rules_template': """
*filter
:INPUT ACCEPT 
:FORWARD ACCEPT 
:OUTPUT ACCEPT 
:whitelist - 
-A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
-A FORWARD -m conntrack --ctstate INVALID -j DROP
-A FORWARD -m mark ! --mark 0 -j ACCEPT
# only mark == 0 from now on
-A FORWARD -j whitelist 
-A FORWARD -j DROP
# a list of connections to allow even for unmarked connections
-A whitelist -p udp --dport 53 -j ACCEPT
-A whitelist -p tcp --dport 53 -j ACCEPT
COMMIT
*mangle
:PREROUTING ACCEPT 
:INPUT ACCEPT 
:FORWARD ACCEPT 
:OUTPUT ACCEPT 
:POSTROUTING ACCEPT 
:authorized - 
-A PREROUTING -j CONNMARK --restore-mark
-A PREROUTING -j authorized
-A POSTROUTING -j CONNMARK --save-mark
COMMIT
*nat
:PREROUTING ACCEPT 
:POSTROUTING ACCEPT 
:OUTPUT ACCEPT
:capture_browser -
:marked_connections -
:whitelist -
-A PREROUTING -m mark ! --mark 0 -j marked_connections
#only mark == 0  from now on
-A PREROUTING -j whitelist
-A PREROUTING -p tcp --dport 80 -j capture_browser
-A POSTROUTING -o %(WAN_IF)s -j SNAT --to-source %(WAN_IP)s
# redirect to transparent proxy and local dns server ?
#-A marked_connections -i %(LAN_IF)s -p tcp --dport 80 -j REDIRECT --to-ports 3129
#-A marked_connections -i %(LAN_IF)s -p tcp --dport 53 -j REDIRECT --to-ports 53
#-A marked_connections -i %(LAN_IF)s -p udp --dport 53 -j REDIRECT --to-ports 53
-A marked_connections -j ACCEPT
# capture browser and log
-A capture_browser -j LOG --log-prefix CAPTURED
-A capture_browser -p tcp --dport 80 -j REDIRECT --to-ports 81
-A whitelist -p tcp --dport 80 -d %(LAN_IP)s -j ACCEPT
COMMIT
"""
``` 
}

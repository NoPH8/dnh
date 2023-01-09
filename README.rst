====
VPN domain name helper
====

What is this?
--------
This is the simple helper for VPN-routing.
You can add domain-names and custom ip-range networks to route through the VPN and get all the list in API endpoint.

Installation
--------
You need to specify .env-file to run the app. There is a template to use as an example.

To create 'SECRET_KEY' and 'SECURITY_PASSWORD_SALT' values you can use pre-installed make-helpers (feel free to use different make-commands: just type `make help` to see all possible commands).

Usage
--------

Create admin-user using ``flask manage createsuperuser`` then login to ``/admin/``.

====
VPN domain name helper
====

.. image:: https://codecov.io/gh/NoPH8/dnh/branch/master/graph/badge.svg?token=C8GfOv84Bu
 :target: https://codecov.io/gh/NoPH8/dnh

What is this?
--------
This is the simple helper for VPN-routing.
You can add domain-names and custom ip-range networks to route through the VPN and
get all the list in API endpoint.

Deployment & configuration
--------
Application can run directly or via docker image.
Edit docker-compose.yml if you need additional configuration.

You need to specify .env-file to run the app.
The default name of .env-file for dockerized app is .env_docker.

There is a template to use as an example.
All possible parameters are in the table below.

+------------------------+----------+-------------------+-----------------------------------------+
|  Parameter             | Required | Default           |         Description                     |
+========================+==========+===================+=========================================+
| APP_NAME               | No       | DNH               | Used in admin panel header              |
+------------------------+----------+-------------------+-----------------------------------------+
| DATETIME_FORMAT        | No       | %Y-%m-%d %H:%M:%S | Default datetime format to show in admin|
+------------------------+----------+-------------------+-----------------------------------------+
| DB_NAME                | No       | database.sqlite   | SQLite database name                    |
+------------------------+----------+-------------------+-----------------------------------------+
| DB_PATH                | No       | {App directory}   | Absolute path to directory with sqlite  |
+------------------------+----------+-------------------+-----------------------------------------+
| DNS_SERVERS            | No       |                   | Used to resolve records domain names.   |
|                        |          |                   | To set many use space as separator      |
+------------------------+----------+-------------------+-----------------------------------------+
| DNS_UPDATE_INTERVAL    | No       | 15                | It shows update interval in minutes.    |
+------------------------+----------+-------------------+-----------------------------------------+
| SECRET_KEY             | Yes      |                   | Secret key for Flask-security purposes. |
|                        |          |                   | See note below the table                |
+------------------------+----------+-------------------+-----------------------------------------+
| SECURITY_PASSWORD_SALT | Yes      |                   | Flask-security password salt.           |
|                        |          |                   | See note below the table                |
+------------------------+----------+-------------------+-----------------------------------------+
| SERVER_TIMEZONE        | No       | UTC               | IANA time zone on server                |
+------------------------+----------+-------------------+-----------------------------------------+
| USER_TIMEZONE          | No       | UTC               | IANA time zone to show for users        |
+------------------------+----------+-------------------+-----------------------------------------+

To create 'SECRET_KEY' and 'SECURITY_PASSWORD_SALT' values you can use pre-installed make-helpers
(feel free to use different make-commands: just type `make help` to see all possible commands).

Usage
--------

Create admin-user using ``flask manage createsuperuser`` then login to ``/admin/``.
Add necessary records with domain names and IP range network.

Create APIKey and use it for API endpoint as shown below:

``/api/v1/ip_list?api_key=your_generated_api_key``

The endpoint also has optional param ``family``. Allowed values are ``ipv4`` or ``ipv6``.

Router configuration
--------

The example OpenWRT WireGuard configuration:

- Openwrt 21.x: https://gist.github.com/NoPH8/14d636e8bd150815eff02e6917f1743a

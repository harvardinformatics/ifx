# ifx.rc application server front-end

ifx.rc is a Django front end for the ifx.rc app server.  Besides links to the various applications on the server, an assortment of additional functionality is available.

REMOTE_USER based authentication is used so that HarvardKey auth can be managed by the webserver

## Development
When doing development, the REMOTE_USER must be set.  This can be done one of two ways:

1. When using the built-in Django WSGI server, you can set the IFX_REMOTE_USER environment variable to some username.  The username must be a valid user in the AD system defined by the RCDCS environment variable or in your /etc/ldap.conf
1. When using the development Dockerfile (Dockerfile-dev), include the user in etc/htpasswd.
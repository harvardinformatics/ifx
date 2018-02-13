from django.contrib import auth
from django.contrib.auth.middleware import RemoteUserMiddleware
from django.core.exceptions import ImproperlyConfigured
from rc.ad import Connection
from rc.ad import user as ADUser
import logging, os
from ifx.settings import AD_ADMIN_GROUPS, DEBUG
from portal.models import Account


logger = logging.getLogger(__name__)


def updateRCAccountInfo(user):
    """
    Fetch data from AD and update local bits
    """
    logger.debug("Searching AD...")
    try:

        # Determine the RC username
        rcusername = None
        rcaccount = None
        # If the account record exists, check it
        try:
            rcaccount = Account.objects.get(user=user)
            rcusername = rcaccount.identifier
        except Account.DoesNotExist:
            pass

        # If not, make a new one
        if rcusername is None:
            rcusername = user.username.split('@', 1)[0]

        conn = Connection()
        us = conn.search(sAMAccountName=rcusername)
        if len(us) > 0:
            logger.debug("Found AD user.  Updating settings")
            if "mail" in us[0][1]:
                user.email = us[0][1]["mail"][0]
            if "givenName" in us[0][1]:
                user.first_name = us[0][1]["givenName"][0]
            if "sn" in us[0][1]:
                user.last_name = us[0][1]["sn"][0]

            # If the user is rc_admin or informatics, they are an admin here
            if ADUser.hasGroups(conn, user.username, AD_ADMIN_GROUPS):
                user.is_superuser = True
            else:
                user.is_superuser = False

            # if ADUser.isEnabled(conn, user.username):
            #     user.is_active = True
            # else:
            #     user.is_active = False

            if rcaccount is None:
                rcaccount = Account(name="RC", identifier=rcusername, user=user)
                rcaccount.save()

            user.save()

    except Exception as e:
        logger.error("Unable to update user information from AD: %s" % str(e))
 

class RemoteUserPlusMiddleware(RemoteUserMiddleware):
    """
    If request.user is not authenticated, then this middleware attempts to
    authenticate the username passed in the ``REMOTE_USER`` request header.
    If authentication is successful, the user is automatically logged in to
    persist the user in the session.

    If it is the first time the user has been seen in the session, an attempt
    is made to fetch name, email, etc. from RC AD.  

    If this works and information is different than what was previously there, 
    the information will be stored and a "please review" flag
    will be added to the user table.
    """

    # Name of request header to grab username from.  This will be the key as
    # used in the request.META dictionary, i.e. the normalization of headers to
    # all uppercase and the addition of "HTTP_" prefix apply.
    header = "HTTP_HKEYMAIL"
    force_logout_if_no_header = True

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            logger.debug("Checking header for REMOTE_USER")
            if DEBUG and os.environ.get("IFX_REMOTE_USER"):
                username = os.environ.get("IFX_REMOTE_USER").strip()
            else:
                username = request.META[self.header]
            logger.debug("User %s logged in" % username)
            for k, v in request.META.iteritems():
                if 'HKEY' in k:
                    logger.debug("%s = %s" % (k, v))
        except KeyError:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            logger.debug("Key error in check for header.  META headers are %s" % "\n".join(request.META.keys()))
            if self.force_logout_if_no_header and request.user.is_authenticated:
                self._remove_invalid_user(request)
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        logger.debug("Checking for authenticated user")
        if request.user.is_authenticated:
            if request.user.get_username() == self.clean_username(username, request):
                return
            else:
                # An authenticated user is associated with the request, but
                # it does not match the authorized user in the header.
                self._remove_invalid_user(request)

        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        logger.debug("User not authenticated.  Trying...")
        user = auth.authenticate(remote_user=username)
        if user:
            logger.debug("User is valid")
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)
            
            updateRCAccountInfo(user)


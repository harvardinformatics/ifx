from django import template
import logging


register = template.Library()
logger = logging.getLogger(__name__)


@register.filter(name="rcusername")
def rcusernameFilter(user):
    rcusername = None
    try:
        rcusername = user.account_set.filter(name="RC")[0].identifier
    except Exception:
        logger.debug("Failed to find RC account.")
    return rcusername

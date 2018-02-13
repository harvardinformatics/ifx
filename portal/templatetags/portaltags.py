from django import template

register = template.Library()

@register.filter(name="rcusername")
def rcusernameFilter(user):
	rcusername = None
	try:
		rcusername = user.account_set.filter(name="RC")[0].identifier
	except Exception:
		pass
	return rcusername

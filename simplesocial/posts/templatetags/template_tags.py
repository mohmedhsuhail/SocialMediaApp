from django import template
register = template.Library()

@register.simple_tag
def flag(value="True"):
	return value
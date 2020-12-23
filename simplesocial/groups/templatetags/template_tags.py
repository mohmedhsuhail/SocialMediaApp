'''from django import template
from ..models import Group,GroupMember

register = template.Library()

@register.inclusion_tag('grouped_list.html')
def Groups(user):
	print(user)
	get_user_groups = Group.objects.filter(members__user__username__contains=user)
	print(get_user_groups)
	get_other_groups = Group.objects.all()

	return {'get_user_groups':get_user_groups,'get_other_groups':get_other_groups}'''
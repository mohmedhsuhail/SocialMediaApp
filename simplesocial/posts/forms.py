from django import forms
from .models import Post
from groups.models import Group,GroupMember

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['message','group']
	def __init__(self,user,*args,**kwargs):																																									
		super(PostForm,self).__init__(*args,**kwargs)
		members = GroupMember.objects.prefetch_related('user').filter(user__username__contains=user)
		members = members.select_related('group')
		group_list = []
		for member in members:
			group_list.append(member.group.name)
		self.fields['group'].queryset = Group.objects.filter(name__in=group_list)
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib import messages
from groups.models import Group,GroupMember
from django.db import IntegrityError
from . import models
from braces.views import PrefetchRelatedMixin
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
User = get_user_model()
# Create your views here.

class CreateGroup(LoginRequiredMixin,generic.CreateView):
	fields = ('name','description')
	model = Group

	def form_valid(self,form):
		user = User.objects.get(username=self.request.user)
		form.instance.admin = user
		form.save()
		return super(CreateGroup, self).form_valid(form)

class SingleGroup(PrefetchRelatedMixin,generic.DetailView):
	model = Group
	prefetch_related = ['posts','members']

class ListGroups(PrefetchRelatedMixin,generic.ListView):
	model = Group
	prefetch_related = ['posts','members']

class JoinGroup(LoginRequiredMixin,generic.RedirectView):

	def get_redirect_url(self,*args,**kwargs):
		return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

	def get(self,request,*args,**kwargs):
		group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

		try:
			GroupMember.objects.create(user=self.request.user,group=group)
		except IntegrityError:
			messages.warning(self.request,"Warning. Already a member")
		else:
			messages.success(self.request,'You are now a member')

		return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):

	def get_redirect_url(self,*args,**kwargs):
		return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

	def get(self,request,*args,**kwargs):

		try:
			membership = models.GroupMember.objects.filter(
					user=self.request.user,
					group__slug=self.kwargs.get('slug')
				).get()

		except models.GroupMember.DoesNotExist:
			messages.warning(self.request,'Sorry. You are not in this group')

		else:
			membership.delete()
			messages.success(self.request,"You have successfully left this group")

		return super().get(request, *args, **kwargs)

def DeleteGroup(request,pk):
	if  request.method == 'GET':
		group = get_object_or_404(Group,pk=pk)
		if group.admin == request.user:
			group.delete()
	return HttpResponseRedirect(reverse('groups:all'))

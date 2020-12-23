from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from braces.views import SelectRelatedMixin
from django.contrib.messages.views import SuccessMessageMixin
from . import models
from . import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from groups.models import GroupMember,Group
from .forms import PostForm
User = get_user_model()

class PostList(SelectRelatedMixin,generic.ListView):
	model = models.Post
	select_related = ('user',)
	template_name = 'post_list'

class UserPosts(SelectRelatedMixin,generic.ListView):
	model = models.Post
	select_related = ('user',)
	template_name = 'posts/user_post_list.html'

	def get_queryset(self):
		try:
			self.post_user = User.objects.get(username__iexact=self.request.user)

		except User.DoesNotExist:
			raise Http404
		else:
			return self.post_user.posts.all()

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['post_user'] = self.post_user
		return context

class PostDetail(SelectRelatedMixin,generic.DetailView):
	model = models.Post
	select_related = ('user','group')

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):

	model = models.Post
	form_class = PostForm

	def get_form_kwargs(self):
		kwargs = super(CreatePost,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self,form):
		self.object = form.save(commit = False)
		self.object.user = self.request.user 
		self.object.save()
		return super().form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
	model = models.Post 
	select_related = ('user','group')
	success_url = reverse_lazy('posts:all')

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(user_id = self.request.user.id)


	def delete(self,*args,**kwargs):
		messages.success(self.request,'deleted')
		return super().delete(*args,**kwargs)

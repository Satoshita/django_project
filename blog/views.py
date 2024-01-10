from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView
	)


# def home(request):
# 	posts = Post.objects.all().order_by('-date_posted')[:]
# 	return render(request, 'home.html', {'posts': posts})


class PostListView(ListView):
	model = Post
	template_name = 'home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 4


class UserPostListView(ListView):
	model = Post
	template_name = 'user_posts.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 3

	#ユーザーモデルからpost.userのオブジェクトをセットする
	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
	model = Post
	template_name = 'detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post 
	fields = ['title', 'content']
	template_name = 'create.html'

	#ユーザーを設定する
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post 
	fields = ['title', 'content']
	template_name = 'create.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	#requestユーザーと投稿者が同一か判定する
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = 'post_confirm_delete.html'
	success_url = reverse_lazy('blog:home')
	
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


@login_required()
def about(request):
	return render(request, 'about.html', {})



#https://www.youtube.com/watch?v=Sa_kQheCnds


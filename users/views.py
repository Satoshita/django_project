from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import TemplateView, PasswordChangeView
# from django.contrib.auth.mixins import PasswordContextMixin



def register(request):
	form = UserRegisterForm()
	if request.method == 'POST':
		form = UserRegisterForm(request.POST or None)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}!')
			return redirect('users:login')
		else:
			form = UserRegisterForm()
	return render(request, 'register.html', {'form': form})


def loginView(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		messages.success(request, f'{username}, Your login successfully!')
		return redirect('blog:home')
	else:
		messages.error(request, None)
	return render(request, 'login.html')


@login_required()
def logoutView(request):
	logout(request)
	return render(request, 'logout.html')


@login_required()
def profileView(request):
	u_form = UserUpdateForm(instance=request.user)
	p_form = ProfileUpdateForm(instance=request.user.profile)
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST or None, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your profile has been updated!')
			return redirect('users:profile')
		else:
			u_form = UserUpdateForm(instance=request.user)
			p_form = ProfileUpdateForm(instance=request.user.profile)
	context = {
		'u_form': u_form, 
		'p_form': p_form,
		}
	return render(request, 'profile.html', context)






from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
	"""logout users"""
	logout(request)
	return HttpResponseRedirect(reverse('learning_logs:index'))

def register(request):
	"""register new user"""
	if request.method != 'POST':
		form = UserCreationForm()
	else:
		# 处理填写好的表单
		form = UserCreationForm(request.POST)

		if form.is_valid():
			new_user = form.save()
			# 让用户自动登录，再重定向到主页
			authenticated_user = authenticate(username=new_user.username,
				password=request.POST['password1'])
			login(request, authenticated_user)
			return HttpResponseRedirect(reverse('learning_logs:index'))

	context = {'form': form}
	return render(request, 'users/register.html', context)

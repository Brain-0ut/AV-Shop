from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as logout_
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView

from users.forms import RegisterForm, EmailConfirmForm
from users.models import User

from django import views


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
            )
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            return redirect('/')
    return render(request, 'users/register.html', {'form': form})


def logout(request):
    logout_(request)
    return redirect('/')


class UserInfo(View):
    template_name = 'users/personal_page.html'

    def get(self, request, *args, **kwargs):
        confirm_form = None
        if not self.request.user.email_confirmed:
            confirm_form = EmailConfirmForm()
        return render(request, self.template_name, {'confirm_form': confirm_form})

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('action') == 'confirm':
            form = EmailConfirmForm(self.request.POST)
            if form.is_valid():
                if form.cleaned_data.get('token') == self.request.user.token:
                    self.request.user.email_confirmed = True
                    self.request.user.save()
            else:
                return render(self.request, self.template_name, {'confirm_form': form})
        return HttpResponseRedirect(reverse('user_info'))

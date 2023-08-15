from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View

from cube import settings

from .forms import LoginForm, RegisterForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class LoginView(View):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()

        if request.user.is_authenticated:
            return redirect('main')
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'main')
                messages.success(request, 'You are now logged in.')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        return render(request, self.template_name, {'form': form})



class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('main')


class RegisterView(View):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('main')

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form})
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.views import generic
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.models import User

from customers.models import Customer

from users.forms import RegisterForm
# Create your views here.
class RegisterView(generic.View):
    template_name = 'register.html'

    def get(self, request, *args, **kwarg):
        return render(request, self.template_name, {'form': RegisterForm()})


    def post(self, request, *args, **kwargs):
        context = {}
        error_message = ''

        form = RegisterForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    user = User()
                    user.username = form.cleaned_data['email']
                    user.email = form.cleaned_data['email']
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.set_password(form.cleaned_data['password'])
                    user.save()

                    customer = Customer.objects.filter(email=user.email).first()

                    if customer:
                        customer.user = user
                        customer.first_name = user.first_name
                        customer.last_name = user.last_name
                        customer.save()
                    else:
                        customer = Customer()
                        customer.user = user
                        customer.first_name = user.first_name
                        customer.last_name = user.last_name
                        customer.email = user.email
                        customer.date_registered = timezone.now()
                        customer.save()

                    return redirect(reverse('users:login'))
            except:
                error_message = 'Something went wrong!'
        

        return render(request, self.template_name, {'form': form, 'error_message': error_message})


class LoginView(generic.View):
    template_name = 'login.html'


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


    def post(self, request, *args, **kwargs):
        context = {}
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect(reverse('index'))
        
        context['error'] = 'Incorrect Email/Password'
        return render(request, self.template_name, context)

    
class LogoutView(generic.View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('index'))


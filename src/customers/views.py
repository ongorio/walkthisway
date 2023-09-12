from typing import Any, Dict
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash

from customers.forms import CustomerEditForm, PasswordUpdateForm

# Create your views here.
class ProfileView(generic.TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        customer = self.request.user.customer
        context['customer'] = customer

        orders = customer.orders.filter(closed=True).order_by('-date_ordered').all()
        context['orders'] = orders

        return context
    

class EditProfileView(generic.View):
    template_name = 'profile_edit.html'
    form_class = CustomerEditForm

    def get_initial_data(self):
        customer = self.request.user

        data = {
            'email': customer.email,
            'first_name': customer.first_name,
            'last_name': customer.last_name
        }

        return data

    def get(self, request, *args, **kwargs):
        context = {}
        
        form = self.form_class(initial=self.get_initial_data())
        context['form'] = form


        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        context = {}
        

        form = self.form_class(data=request.POST, initial=self.get_initial_data())
        
        if form.is_valid():
            user = request.user
            customer = user.customer


            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            customer.first_name = first_name
            customer.last_name = last_name
            customer.save()

            return redirect(reverse('customers:profile'))
        else:
            print(form.errors)

        context['form'] = form


        return render(request, self.template_name, context)
    

class ProfileUpdatePasswordView(generic.View):
    template_name = 'profile_edit.html'
    form_class = PasswordUpdateForm

    def get(self, request, *args, **kwargs):
        context = {}
        form = self.form_class(user=request.user)
        context['form'] = form

        return render(request, self.template_name, context)
    

    def post(self, request, *args, **kwargs):
        context = {}
        user = request.user
        form = self.form_class(request.POST, user=user)

        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)

            return redirect(reverse('customers:profile'))
        
        else:
            print(form.errors)

        context['form'] = form

        return render(request, self.template_name, context)


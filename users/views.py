from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib.auth import login, get_backends

from .forms import CustomerSignUpForm, CompanySignUpForm
from .models import User


# =================================================================================================


# CHOOSE TYPE OF USER TO REGISTER
def register(request):
    return render(request, "users/register.html")


# the following 2 classes work as the login function but for register. The reason
# we use a class instead of a function while calling the appropriate form (class),is that
# the registration process is more complicated
# | | |
# v v v

# =================================================================================================


# CUSTOMER REGISTRATION
class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = "users/register_customer.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "customer"
        return super().get_context_data(**kwargs)
        # this is used to add extra information to the context that will be passed to
        # the template (user = customer)

    def form_valid(self, form):  # this form argument is the validated instance of the CustomerSignUpForm
        if form.is_valid():
            user = form.save()

            backend = get_backends()[0]
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            # we tell Django to use the first authentication backend in settings.py / AUTHENTICATION_BACKENDS

            login(self.request, user)  # he is immediatly logged in here
            return redirect("/")
        else:
            return self.form_invalid(form)

    #  Django, internally knows and handles:
    #  when the page opens first time, the method is GET and get_context_data runs
    #  when the client submits his form, the method is POST and form_valid runs


# =================================================================================================


# COMPANY REGISTRATION
class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = "users/register_company.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "company"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()

            backend = get_backends()[0]
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

            login(self.request, user)
            return redirect("/")
        else:
            return self.form_invalid(form)

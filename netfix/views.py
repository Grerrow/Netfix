from django.shortcuts import render, redirect
from datetime import date
from django.contrib import admin
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from users.models import User, Company, Customer
from services.models import Service, RequestService

from django.contrib.auth.decorators import login_required, user_passes_test

def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year


@login_required
# this decorator automatically redirects to login page any non-authenticated user
# if he tries to open any customer profile page even if he types /customer/user_name in the url
# otherwise it would return to Homepage from the if condition below
@never_cache
# this decorator ensures that no customer profile page is saved to cache, so if the user1 logs out
# the next one, user2, cant go back using browser's history to check user1's profile
def customer_profile(request, name):
    if request.user.username != name:
        return redirect("/")
    # with this if condition we are sure each user can only open his own profile page,
    # even if he types /customer/user_name in the url

    user = User.objects.get(username=name)
    customer = Customer.objects.get(user=user)

    user_age = calculate_age(customer.date_of_birth)
    requested_services = RequestService.objects.filter(customer=customer).order_by("-requested_date")

    return render(request, "users/profile.html", {"user": user, "requested_services": requested_services, "user_age": user_age})


def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = User.objects.get(username=name)
    services = Service.objects.filter(company=Company.objects.get(user=user)).order_by("-date")

    return render(request, "users/profile.html", {"user": user, "services": services})
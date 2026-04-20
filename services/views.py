from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count

from users.models import Company
from services.models import Service, RequestService

from services.forms import CreateNewService, RequestServiceForm


def list_of_services(request):
    services = Service.objects.all().order_by("-date")
    return render(request, "services/list_of_services.html", {"services": services})


def single_service(request, id):
    service = Service.objects.get(id=id)  # get the service by ID
    return render(request, "services/single_service.html", {"service": service})


def services_per_field(request, field):
    # search for the service present in the url
    field = field.replace("-", " ").title()
    services = Service.objects.filter(field=field)
    return render(request, "services/services_per_field.html", {"services": services, "field": field})


def most_requested_services(request):
    services = (Service.objects
                .annotate(request_count=Count("requestservice"))
                .order_by("-request_count")[:10]
                )
    # - annotate() adds aggregated data (like sums, counts, averages) to each object in the queryset
    # - Count("requestservice") counts how many related RequestService entries are linked to each Service
    # stores the result in a new attribute called request_count.
    # - "requestservice" refers to the reverse ForeignKey relationship from RequestService to Service
    # Django auto-generates this name based on the model name (requestservice_set by default)
    # - this uses Django's ORM to perform a SQL JOIN and COUNT.

    return render(request, "services/most_requested.html", {"services": services})


def create_service(request):
    if request.method == "POST":
        # if the request is POST, this creates an instance of CreateNewService form
        # with all the data input from the user

        company = Company.objects.get(user=request.user)
        company_field = company.field

        #  the request.POST contains all the data submitted by the user
        form = CreateNewService(request.POST, company_field=company_field)
        if form.is_valid():
            # if the form is valid a new Service object is created and saved to the database
            Service.objects.create(
                company=company,
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                price_hour=form.cleaned_data["price_hour"],
                field=form.cleaned_data["field"],
            )
            return redirect("services_list")
        # else:
        #     print(form.errors)
    else:
        company = Company.objects.get(user=request.user)
        company_field = company.field
        form = CreateNewService(company_field=company_field)

    return render(request, "services/create_service.html", {"form": form})


def request_service(request, id):
    service = get_object_or_404(Service, pk=id)

    if request.method == "POST":
        form = RequestServiceForm(request.POST)

        if form.is_valid():
            customer = request.user.customer
            service_hours = form.cleaned_data["service_hours"]

            calculated_cost = service.price_hour * service_hours

            RequestService.objects.create(
                service=service,
                customer=customer,
                calculated_cost=calculated_cost,
                service_hours=service_hours,
                company=service.company,
            )

            return redirect("customer_profile", name=request.user.username)
            # in redirect() the first argument should be a view:
            # using "return redirect("customer_profile", name=request.user.username), we are
            # telling Django to use the name of the view ("customer_profile" or "company_profile")
            # and resolve the full URL for that view dynamically. Django will use the URL pattern
            # associated with that view name and generate the corresponding URL using the parameters
            # (like name=request.user.username) you provide.
            # This does NOT work: "return redirect("customer/<slug:name>", name=request.user.username)"
            # in login form we can use "return redirect("/") because we tell Django to serve
            # a static (home) page

    else:
        form = RequestServiceForm()

    return render(request, "services/request_service.html", {"form": form, "service": service})


# get() vs get_object_or_404():
# -----------------------------

# in create_service view the company we request with get is the one that is already registered and logged in, so there
# is no chance we cant get that Comapny object
# on the other hand when we request a Service object by id, we can request something that doesnt exist,
# for example the client can try an id number in the url that doesnt correspond to a Service





# =====================================================================================================================

# this was a much more complicated way to do it, with 2 queries
# when to use:
    # if advanced calculations across multiple models (e.g., combining multiple foreign keys) were needed
    # when dealing with non-related models (if requestservice wasn’t a direct relation to Service)
    # when using custom aggregation beyond what .annotate() can do

# def most_requested_services2(request):
#     most_requested = (
#         RequestService.objects.values("service")
#         # group by Service foreign key
#         .annotate(request_count=Count("service"))
#         # count requests per service
#         # Count: An aggregation function from Django’s django.db.models—used to count records in the database
#         .order_by("-request_count")[:10]
#         # order by most requested
#     )

#     services = Service.objects.filter(id__in=[item["service"] for item in most_requested])
#     # its better to get the actual Service objects for display by filtering with the service IDs from the
#     #  first query. This lets us access all Service attributes (name, description, etc)
#     # what this line does:
#     # -- each item in most_requested is a dictionary with these keys: {'service': 3, 'request_count': 15}
#     # -- item["service"] represents the ID of the requested service
#     # -- list comprehension: it creates a list of service IDs from the most_requested queryset. Example: [3, 7, 12, 4, 9]
#     # -- id__in: This is a Django lookup that filters by a list of values (SQL IN clause):
#     # SELECT * FROM service
#     # WHERE id IN (3, 7, 12, 4, 9)
#     # so services actually return something like this:
#     # <QuerySet [
#     #     <Service: Cleaning (id=3)>,
#     #     <Service: Plumbing (id=7)>,
#     #     <Service: Gardening (id=12)>
#     #  ]>

#     service_counts = {item["service"]: item["request_count"] for item in most_requested}
#     # this is a dictionary where we link each service with its request_count
#     # so service_counts actually return something like this:
#     # {
#     #     3: 15,  service ID 3: 15 requests
#     #     7: 9,   service ID 7: 9 requests
#     #     12: 5   service ID 12: 5 requests
#     # }

#     services_with_counts = [{"service": service, "request_count": service_counts[service.id]} for service in services]
#     # we create a list of dictionaries, each one containing both the service object and its request_count
#     # so services_with_counts actually return something like this:
#     #     [
#     #     {"service": <Service: Cleaning (id=3)>,
#     #       "request_count": 15
#     #     },
#     #     {"service": <Service: Plumbing (id=7)>,
#     #      "request_count": 9
#     #     },
#     #     {"service": <Service: Gardening (id=12)>,
#     #      "request_count": 5
#     #     }
#     # ]

#     return render(request, "services/most_requested.html", {"services": services_with_counts})

from django import forms

from .models import Service, RequestService


class CreateNewService(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    price_hour = forms.DecimalField(max_digits=100, decimal_places=2)
    field = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        company_field = kwargs.pop("company_field", None)

        super().__init__(*args, **kwargs)

        if company_field == "All in One":
            self.fields["field"].choices = Service.choices
        else:
            self.fields["field"].choices = [(company_field, company_field)]

        # adding placeholders to the fields
        self.fields["name"].widget.attrs["placeholder"] = "Enter Service Name"
        self.fields["description"].widget.attrs["placeholder"] = "Enter Description"
        self.fields["price_hour"].widget.attrs["placeholder"] = "Enter Price per Hour"

        self.fields["name"].widget.attrs["autocomplete"] = "off"
        self.fields["description"].widget.attrs["autocomplete"] = "off"
        self.fields["price_hour"].widget.attrs["autocomplete"] = "off"


class RequestServiceForm(forms.ModelForm):
    address = forms.CharField(max_length=100)
    # we dont have to declare service_hours because it is declared in the request_service model

    class Meta:
        # class Meta is how you tell Django which model the form is for and which fields should be included in the form.
        model = RequestService
        fields = ["service_hours", "address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service_hours"].widget.attrs["placeholder"] = "Enter Service Hours"
        self.fields["address"].widget.attrs["placeholder"] = "Enter Address"


# forms.ModelForm vs forms.Form:
# ------------------------------

# ModelForm: when the form directly represents a model and we intend to save data to that model
# also it is easier to maintain. If your model changes, the form adapts more easily

# Form: when the form does not directly map to a model or requires custom logic unrelated to a model
# also when form fields are dynamic (e.g., __init__ logic to set choices based on context like
# the company_field in the CreateNewService form)
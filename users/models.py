from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # The OneToOneField is a type of database relationship in Django. It's used to create
    # a one-to-one relationship between two models, meaning each record in the first model
    # corresponds to exactly one record in the second model, and vice versa
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.user.id) + " -  " + self.user.username


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    field = models.CharField(
        max_length=70,
        choices=(
            ("Air Conditioner", "Air Conditioner"),
            ("All in One", "All in One"),
            ("Carpentry", "Carpentry"),
            ("Electricity", "Electricity"),
            ("Gardening", "Gardening"),
            ("Home Machines", "Home Machines"),
            ("House Keeping", "House Keeping"),
            ("Interior Design", "Interior Design"),
            ("Locks", "Locks"),
            ("Painting", "Painting"),
            ("Plumbing", "Plumbing"),
            ("Water Heaters", "Water Heaters"),
        ),
        blank=False,
        null=False,
    )
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], default=0)

    def __str__(self):
        return str(self.user.id) + " - " + self.user.username

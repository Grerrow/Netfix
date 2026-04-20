from django.apps import AppConfig


class ServicesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "services"


# In Django, the apps.py file is used to configure settings for a particular app in your project.
# Settings like: default_auto_field or app name

# default_auto_field = "django.db.models.BigAutoField": This setting specifies the default field type
# for automatically incrementing primary keys (IDs) in models. The BigAutoField type is an integer that
# auto-increments with a larger range (64-bit).

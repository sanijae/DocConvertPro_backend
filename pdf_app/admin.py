from django.contrib import admin
from django.apps import apps
from adminplus.sites import AdminSitePlus

# admin.site = AdminSitePlus()
def register_all_models():
    for model in apps.get_models():
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass

register_all_models()
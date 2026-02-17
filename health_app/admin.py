from django.contrib import admin
from .models import RealEstate
# Register your models here.

#admin.site.register(RealEstate)

@admin.register(RealEstate)
class RealEstateAdmin(admin.ModelAdmin):
    list_display = ("id", "area", "bedrooms", "bathrooms", "stories", "price", "user")
    list_filter = ("furnishingstatus", "mainroad", "prefarea")
    search_fields = ("area", "bedrooms", "bathrooms", "stories", "user")

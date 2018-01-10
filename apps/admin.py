from django.contrib import admin
from .models import *
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ["created_by", "id_num", "phone"]
    search_fields = ["id_num", "phone", "address"]
    list_filter = ["gender"]

    class Meta:
        model = Customer

admin.site.register(Customer, CustomerAdmin)  

class FacilityAdmin(admin.ModelAdmin):
    list_display = ["display_name", "short_name", "description"]
    search_fields = ["display_name", "short_name", "description"]

    class Meta:
        model = Facility

admin.site.register(Facility, FacilityAdmin)


class VolumeAdmin(admin.ModelAdmin):
    list_display = ["display_name", "area_wide", "address"]
    search_fields = ["display_name", "address", "desc"]

    class Meta:
        model = Volume

admin.site.register(Volume, VolumeAdmin)  


class WitnessAdmin(admin.ModelAdmin):
    list_display = ["fullname", "id_num", "address"]
    search_fields = ["fullname", "id_num", "address"]

    class Meta:
        model = Witness

admin.site.register(Witness, WitnessAdmin)  


class FileAdmin(admin.ModelAdmin):
    list_display = ["display_name", "short_name"]
    search_fields = ["display_name", "short_name"]

    class Meta:
        model = File

admin.site.register(File, FileAdmin)   


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["customer", "volume", "reg_id", "reg_behalf"]
    search_fields = ["customer__created_by__first_name", "customer__created_by__last_name", "volume__display_name", "reg_id", "reg_behalf"]
    list_filter = ["volume", "due_date"]

    class Meta:
        model = Purchase

admin.site.register(Purchase, PurchaseAdmin)  


class InstallmentAdmin(admin.ModelAdmin):
    list_display = ["customer", "order", "purchase"]
    search_fields = ["customer__created_by__first_name", "customer__created_by__last_name", "order", "purchase__installment_total"]

    class Meta:
        model = Installment

admin.site.register(Installment, InstallmentAdmin)   


class FinanceAdmin(admin.ModelAdmin):
    list_display = ["description", "value"]
    search_fields = ["description", "value"]

    class Meta:
        model = Finance

admin.site.register(Finance, FinanceAdmin)   
        
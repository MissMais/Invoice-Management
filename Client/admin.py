from django.contrib import admin
from .models import *

# Register your models here.

 

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = Client.DisplayField
    
@admin.register(Technology_option)
class Technology_optionAdmin(admin.ModelAdmin):
    list_display = Technology_option.DisplayField


@admin.register(Technology)
class TechnolongyAdmin(admin.ModelAdmin):
    list_display = Technology.DisplayField


@admin.register(Payment_method)
class Payment_mthodAdmin(admin.ModelAdmin):
    list_display = Payment_method.DisplayField


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = Tax.DisplayField

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = Team.DisplayField
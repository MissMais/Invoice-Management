from django.contrib import admin
from .models import *



@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = Client.DisplayField
@admin.register(CompanyDetails)
class CompanyDetailsAdmin(admin.ModelAdmin):
    list_display = CompanyDetails.DisplayField
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
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = Invoice.DisplayField
    list_editable=['generated_date']
@admin.register(Invoice_item)
class Invoice_itemAdmin(admin.ModelAdmin):
    list_display = Invoice_item.DisplayField
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = Team.DisplayField
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = Project.DisplayField
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = Payment.DisplayField
import django_filters
from  .models import *

class ClientFilter(django_filters.FilterSet):
    client_name = django_filters.CharFilter(field_name='client_name', lookup_expr='istartswith')
    client_id = django_filters.NumberFilter(field_name='client_id', lookup_expr='istartswith')
    user_name = django_filters.CharFilter(field_name='user_id__user_name', lookup_expr='istartswith')
    company_address = django_filters.CharFilter(field_name='company_address',lookup_expr='istartswith')

    

    class Meta:
        model = Client
        fields = ['client_name','client_id','user_name','company_address']



class ProjectFilter(django_filters.FilterSet):
    project_name = django_filters.CharFilter(field_name='project_name', lookup_expr='istartswith')
    project_id = django_filters.NumberFilter(field_name='project_id')
    duration = django_filters.CharFilter(field_name='duration',lookup_expr='istartswith')
    client_id = django_filters.NumberFilter(field_name='client_id')
    team_id = django_filters.NumberFilter(field_name='team_id')
    tech_id = django_filters.NumberFilter(field_name='tech_id')

    class Meta:
        model = Project
        fields = ['project_name','project_id','duration','client_id','team_id','tech_id']




class InvoiceFilter(django_filters.FilterSet):
    invoice_id = django_filters.NumberFilter(field_name='invoice_id')
    client_name = django_filters.CharFilter(field_name='client_id__client_name',lookup_expr='istartswith')
    due_date = django_filters.DateFilter(field_name='due_date')
    total_amount = django_filters.NumberFilter(field_name='total_amount')
    status = django_filters.CharFilter(field_name='status',lookup_expr='istartswith')


    class Meta:
        model = Invoice
        fields = ['invoice_id','client_name','due_date','total_amount','status']

class TechnologyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name',lookup_expr='istartswith')

    class Meta:
        model = Technology
        fields = ['name']



class TeamFilter(django_filters.FilterSet):
    team_name = django_filters.CharFilter(field_name='team_name',lookup_expr='icontains')

    class Meta:
        model = Team
        fields = ['team_name']



class PaymentFilter(django_filters.FilterSet):
    payment_date = django_filters.DateFilter(field_name='payment_date',lookup_expr='icontains')

    class Meta:
        model = Payment
        fields = ['payment_date']
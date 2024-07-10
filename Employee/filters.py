import django_filters
from .models import * 

class EmployeeFilter(django_filters.FilterSet):
    address = django_filters.CharFilter(field_name='address',lookup_expr= 'istartswith')
    employee_id = django_filters.NumberFilter(field_name='employee_id')
    user_name = django_filters.CharFilter(field_name='user_id__user_name',lookup_expr='istartswith')
    age = django_filters.NumberFilter(field_name='age')
    salary = django_filters.NumberFilter(field_name='salary')
    id_proof = django_filters.CharFilter(field_name='id_proof',lookup_expr='istartswith')
    pincode = django_filters.NumberFilter(field_name='pincode')
    city_id = django_filters.NumberFilter(field_name='city_id')
    state_id = django_filters.NumberFilter(field_name='state_id')
    country_id = django_filters.CharFilter(field_name='country_id')
    role_id = django_filters.CharFilter(field_name='role_id')



    class Meta:
        model = Employee
        fields = ['address','employee_id','user_name','age','salary','id_proof','pincode',
                  'city_id','state_id','country_id','role_id']
        
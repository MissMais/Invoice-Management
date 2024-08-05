from rest_framework import routers, serializers,viewsets
from .models import*
from Auth_user.serializer import *
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail




class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        
class CompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class InvoiceitemSerializer(serializers.ModelSerializer):
    project_name=serializers.CharField(source='project_id.project_name',read_only=True)
    tax_name=serializers.CharField(source='tax_id.tax_name',read_only=True)
    tax_rate=serializers.IntegerField(source='tax_id.rate',read_only=True)
    class Meta:
        model = Invoice_item
        fields = '__all__'
class InvoiceSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client_id.client_name',read_only=True)
    client_email = serializers.CharField(source='client_id.email',read_only=True)
    client_contact = serializers.CharField(source='client_id.contact',read_only=True)
    client_address = serializers.CharField(source='client_id.address',read_only=True)
    client_pincode = serializers.CharField(source='client_id.pincode',read_only=True)
    invoice_item_id= InvoiceitemSerializer(read_only=True,many=True)
    class Meta:
        model = Invoice
        fields = ['invoice_id','invoice_number','client_id','client_name','client_email','client_contact','client_address','client_pincode','generated_date','invoice_pdf','total_amount','status','invoice_item_id']
        # fields = "__all__"
    
        
class Technology_optionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology_option
        fields = '__all__'




class TechnologySerializer(serializers.ModelSerializer):
    option_name = serializers.CharField(source='option_id.option',read_only=True)
    class Meta:
        model = Technology
        fields =['tech_id','name','option_id','option_name']



class Payment_methodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment_method
        fields = '__all__'



class TaxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tax
        fields = '__all__'





class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'



class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

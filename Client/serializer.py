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






class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
     




class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields=("email")


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True,min_length=1)

    class Meta:
        field =("new_password")

    def validate(self,data):

        new_password = data.get("new_password")
        token = self.context.get("kwargs").get("token")
        user_id_encode = self.context.get("kwargs").get("user_id_encode")

        if token is None or user_id_encode is None:
            raise serializers.ValidationError("Missing data")
        
        user_id_decode = urlsafe_base64_decode(user_id_encode).decode()
        user = CoreUser.objects.get(user_id=user_id_decode)

        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError("the reset token is invalid")
        
        user.set_password(new_password)
        user.save()
        return data






class InvoiceSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client_id.client_name',read_only=True)
    class Meta:
        model = Invoice
        fields = "__all__"
    
        
        
        
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


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'



class Invoice_create_itemSerializer(serializers.ModelSerializer):
    invoice_id = Invoice()

    class Meta:
        model = Invoice_item
        fileds = '__all__'
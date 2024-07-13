from rest_framework import routers, serializers,viewsets
from.models import*
from Auth_user.serializer import *




class ClientSerializer(serializers.ModelSerializer):
    user_id =CoreUserSerializer()
    class Meta:
        model = Client
        fields = '__all__'
     



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
    tech_id = serializers.StringRelatedField(read_only=True,many=True)
    class Meta:
        model = Project
        fields = '__all__'


class InvoiceitemSerializer(serializers.ModelSerializer):


    class Meta:
        model = Invoice_item
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

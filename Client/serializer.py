from rest_framework import routers, serializers,viewsets
from.models import*
from Auth_user.serializer import *




class ClientSerializer(serializers.ModelSerializer):
    user_id =CoreUserSerializer()
    class Meta:
        model = Client
        fields = '__all__'
        
        
class Technology_optionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Technology_option
        fields = '__all__'




class TechnologySerializer(serializers.ModelSerializer):

    class Meta:
        model = Technology
        fields = '__all__'



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

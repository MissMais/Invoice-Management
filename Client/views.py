from rest_framework.response import Response
from .models import * 
from .serializer import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404



class ClientAPI(APIView):
    def get(self,request):
        client_obj = Client.objects.all()
        client_serializer = ClientSerializer(client_obj,many=True)
        return Response(client_serializer.data)
    
    def post(self,request):
        validated_data = request.data 
        client_serializer = ClientSerializer(data=validated_data)
        if client_serializer.is_valid():
            user_data = validated_data.pop('user_id')
            user_obj = CoreUser.objects.create(**user_data)
            user_obj.set_password(user_data['password'])
            user_obj.save()
            client_obj = Client.objects.create(user_id=user_obj,**validated_data)
            
            return Response({"Message":"Client created successfully"}
                            )
        return Response({"Message":client_serializer.errors})    
        


class Technology_optionViewSet(viewsets.ModelViewSet):
    queryset = Technology_option.objects.all()
    serializer_class = Technology_optionSerializer
    

class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    

class Payment_methodViewSet(viewsets.ModelViewSet):
    queryset = Payment_method.objects.all()
    serializer_class = Payment_methodSerializer



class TaxViewSet(viewsets.ModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer





    


 

 
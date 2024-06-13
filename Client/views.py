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




class TeamAPIView(APIView):
    def get(self, request):
        team = Team.objects.all()
        serializer = TeamSerializer(team, many=True)
        return Response(serializer.data)

    def post(self, request):
        validated_data = request.data
        serializer_obj = TeamSerializer(data=validated_data)

        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response({"message":"team create successfully","Data":serializer_obj.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request):
        validated_data = request.data
        team = Team.objects.get(team_id=validated_data['team_id'])
        serializer_obj = TeamSerializer(team, data=request.data)

        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response({"Message":"Team update Successfully ","Data":serializer_obj.data})
        else:
            return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self,request):
        delete = request.GET.get('delete')
        if delete:
            team_obj = Team.objects.get(team_id=delete)
            team_obj.delete()
            return Response({"message":"Data deleted successfully"},status=status.HTTP_204_NO_CONTENT)
 





class ProjectAPIView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        validated_data = request.data
        serializer_obj = ProjectSerializer(data=validated_data)

        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response({"message":"project create successfully","Data":serializer_obj.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request):
        validated_data = request.data
        project_obj = Project.objects.get(project_id = validated_data['project_id']) 
        serializer_obj = ProjectSerializer(project_obj, data=validated_data)

        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response({"message":"Project update successfully","Data":serializer_obj.data})
        else:
            return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self,request):
        delete = request.GET.get('delete')
        if delete:
            project_obj = Project.objects.get(project_id = delete)
            project_obj.delete()
            return Response({"message":"data deleted successfully "},status=status.HTTP_204_NO_CONTENT)
 
    


 

 
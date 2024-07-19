from django.shortcuts import render
from rest_framework.response import Response
from .models import * 
from .serializer import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import *
from Auth_user.permissions import IsEmployeeOwner
from django.conf import settings
from django.core.mail import EmailMessage
from . import serializer
from rest_framework import response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from Auth_user.models import CoreUser






class EmployeeAPI(APIView):
    
    authentication_classes=[JWTAuthentication]
    
    permission_classes=[IsAuthenticated,IsEmployeeOwner]

    def get(self,request):
        employee_obj = Employee.objects.all()
        employee_serializer = EmployeeSerializer(employee_obj,many=True)
        return Response(employee_serializer.data)
    
    def post(self,request):
        validated_data = request.data 
        employee_serializer = EmployeeSerializer(data=validated_data)
        if employee_serializer.is_valid():
            user_data = validated_data.pop('user_id')
            user_obj = CoreUser.objects.create(
                                                user_name=user_data.get("user_name"),
                                                first_name=user_data.get("first_name"),
                                                last_name=user_data.get("last_name"),
                                                email=user_data.get("email"),
                                                contact=user_data.get("contact"),
                                                is_employee=True
                                                )
            user_obj.set_password(user_data['password'])
            user_obj.save()
            
            city_obj = City.objects.get(city_id=validated_data['city_id'])
            state_obj = State.objects.get(state_id=validated_data['state_id'])
            country_obj = Country.objects.get(country_id=validated_data['country_id'])
            role_obj = Role.objects.get(role_id=validated_data['role_id'])
           
            employee_obj = Employee.objects.create(user_id=user_obj, 
                                                   city_id = city_obj,
                                                   state_id = state_obj,
                                                   country_id = country_obj,
                                                   role_id = role_obj,
                                                   pincode=validated_data['pincode'],
                                                   address=validated_data['address'],
                                                   id_proof=validated_data['id_proof'],
                                                   salary=validated_data['salary'],
                                                   age=validated_data['age'])
            

            email = user_data['email']
            message = EmailMessage(
                'Test email subject',
                'test email body,  client create successfully ',
                settings.EMAIL_HOST_USER,
                [email]
            )
            message.send(fail_silently=False)
            
            return Response({"Message":"Employee created successfully"})
        
        else:
            return Response({"Message":employee_serializer.errors})  
    


    def put(self,request):
        validated_data = request.data
        employee_obj = Employee.objects.get(employee_id=validated_data['employee_id'])
       
        employee_serializer = EmployeeSerializer(employee_obj,data=validated_data,partial=True)
        
        if employee_serializer.is_valid():
            employee_serializer.save()
            return Response({"message":"data updated successfully","data":employee_serializer.data} )
        
        else:
            return Response(employee_serializer.errors)  
     
    def delete(self,request):
        delete_employee = request.GET.get('delete_employee')
        employee_obj = Employee.objects.get(employee_id=delete_employee)
        employee_obj.delete()
        return Response({'Message':"Employee deleted successfully"})



class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [ SearchFilter, DjangoFilterBackend]
    filterset_class = EmployeeFilter







class ChangePasswordView(APIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        data = request.data
        user_obj = self.request.user
        change_serializer=ChangePasswordSerializer(data=data)
        # print('\n\n\n',user_obj,'\n\n\n')

        if change_serializer.is_valid():

            if not user_obj.check_password(data["old_password"]):
                return Response({"old_password":["Wrong Password"]})
            
            user_obj.set_password(data["new_password"])
            user_obj.save()

            response = {
                "password updated successfully"
            }

            return Response(response)
        
        return Response(change_serializer.errors)










class PasswordReset(generics.GenericAPIView):

    serializer_class = serializer.EmailSerializer

    def post(self, request):
      
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = CoreUser.objects.filter(email=email).first()
       
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url = reverse(
                "reset-password",
                kwargs={"encoded_pk": encoded_pk, "token": token},
            )
            reset_link = f"localhost:8000{reset_url}"
             

            # send the reset_link as mail to the user.

            return response.Response(
                {
                    "message": 
                    f"Your password rest link: {reset_link}"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                {"message": "User doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )




class ResetPasswordAPI(generics.GenericAPIView):
   
    serializer_class = serializer.ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
       
         
        serializer = self.serializer_class(
            data=request.data, context={"kwargs": kwargs}
        )

        serializer.is_valid(raise_exception=True)
        return response.Response(
            {"message": "Password reset complete"},
            status=status.HTTP_200_OK,
        )
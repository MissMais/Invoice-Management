from .models import *
from .serializer import *
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication






@api_view(['GET','POST'])
def get_coreuser(request):
    if request.method == "GET":
        try:  
            obj = CoreUser.objects.all()
            ser = CoreUserSerializer(obj,many=True)
            return Response(ser.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == "POST":
        try:
            validated = request.data
            user_serializer = CoreUserSerializer(data=validated)
            if user_serializer.is_valid():
                user_obj = CoreUser.objects.create(**validated)
                user_obj.set_password(validated['password'])
                user_obj.save()
                return Response("User registered successfully",status=status.HTTP_201_CREATED)
            else :
                return Response(user_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class LoginView(APIView):
    def post(self,request):
        try:
            data = request.data 
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                try:
                    username = serializer.data['username']
                    password = serializer.data['password']
                    user = authenticate(username=username,password=password)
                    if user is None:
                        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
                    refresh = RefreshToken.for_user(user)
                    access_token = refresh.access_token
                    custom_claims = access_token.get('custom_claims', {})
                    custom_claims['user_id'] = user.user_id
                    custom_claims['first_name'] = user.first_name
                    custom_claims['last_name'] = user.last_name
                    access_token['custom_claims'] = custom_claims
                    print({'refresh': str(refresh),
                        'access': str(access_token)})
                    return Response({
                        'refresh': str(refresh),
                        'access': str(access_token),
                        # 'user': custom_claims
                    }) 
                except Exception as e:
                    return Response({"error": f"Error during authentication: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)      
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
 
class Logout(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print('\n\n\n',request.data,'\n\n\n')
        
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"Message":"Enter refresh_token"})
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message":"Success"},
                            status=status.HTTP_200_OK
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
        
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer